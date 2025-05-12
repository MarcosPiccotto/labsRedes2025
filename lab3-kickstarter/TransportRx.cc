#ifndef TRANSPORT_RX
#define TRANSPORT_RX

#include <string.h>
#include <omnetpp.h>
#include "FeedbackPkt_m.h"
#include "DataPkt_m.h"

using namespace omnetpp;

class TransportRx : public cSimpleModule
{
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector packetDropVector;
    cOutVector bufferSizeVector;
    int packetDropped;
public:
    TransportRx();
    virtual ~TransportRx();

protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
    void checkAndSendFeedback();
    void sendFeedback(DataPkt *msg);
};

Define_Module(TransportRx);

TransportRx::TransportRx()
{
    endServiceEvent = NULL;
}

TransportRx::~TransportRx()
{
    cancelAndDelete(endServiceEvent);
}

void TransportRx::initialize()
{
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    packetDropVector.setName("packet dropped");
    bufferSizeVector.setName("buffer size");
    packetDropped = 0;
}

void TransportRx::finish()
{
}

void TransportRx::sendFeedback(DataPkt *msg)
{
    FeedbackPkt *feedbackPkt = new FeedbackPkt();

    feedbackPkt->setByteLength(20);
    feedbackPkt->setKind(FEEDBACK);
    feedbackPkt->setCurrentBufferSize(buffer.getLength());
    feedbackPkt->setBufferSize(par("bufferSize").intValue());
    simtime_t delay = simTime() - msg->getTimeStampTx();
    feedbackPkt->setTimeStampRx(delay);

    send(feedbackPkt, "toApp");
}

void TransportRx::handleMessage(cMessage *msg)
{
    if (msg == endServiceEvent)
    {
        if (!buffer.isEmpty())
        {
            DataPkt *pkt = dynamic_cast<DataPkt *>(buffer.pop());
            send(pkt, "toOut$o");
            serviceTime = pkt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);

            sendFeedback(pkt);
        }
    }
    else if (msg->getKind() == 0)
    {
        if (buffer.getLength() >= par("bufferSize").intValue())
        {
            delete msg;
            this->bubble("packet dropped");
            packetDropVector.record(++packetDropped);
        }
        else
        {
            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());
            if (!endServiceEvent->isScheduled())
            {
                scheduleAt(simTime(), endServiceEvent);
            }
        }
    }
}

#endif /* TRANSPORT_RX */
