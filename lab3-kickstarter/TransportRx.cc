#ifndef TRANSPORT_RX
#define TRANSPORT_RX

#include <string.h>
#include <omnetpp.h>
#include "FeedbackPkt_m.h"

using namespace omnetpp;

class TransportRx : public cSimpleModule
{
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;

public:
    TransportRx();
    virtual ~TransportRx();

protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
    void checkAndSendFeedback();
    void sendFeedback();
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
}

void TransportRx::finish()
{
}

void TransportRx::sendFeedback()
{
    FeedbackPkt *feedbackPkt = new FeedbackPkt();

    feedbackPkt->setByteLength(20);
    feedbackPkt->setKind(FEEDBACK);
    feedbackPkt->setCurrentBufferSize(buffer.getLength());
    feedbackPkt->setBufferSize(par("bufferSize").intValue());
    send(feedbackPkt, "toApp");
//    feedbackPkt->setFeedbackStatus(status);
//    lastFeedbackSent = status;
}

void TransportRx::handleMessage(cMessage *msg)
{
    if (msg == endServiceEvent)
    {
        if (!buffer.isEmpty())
        {
            cPacket *pkt = dynamic_cast<cPacket *>(buffer.pop());
            send(pkt, "toOut$o");
            serviceTime = pkt->getDuration();
            scheduleAt(simTime() + serviceTime, endServiceEvent);

            sendFeedback();
        }
    }
    else if (msg->getKind() == 0)
    {
        if (buffer.getLength() >= par("bufferSize").intValue())
        {
            delete msg;
            this->bubble("packet dropped");
        }
        else
        {
            buffer.insert(msg);
            if (!endServiceEvent->isScheduled())
            {
                scheduleAt(simTime(), endServiceEvent);
            }

            sendFeedback();
        }
    }
}

#endif /* TRANSPORT_RX */
