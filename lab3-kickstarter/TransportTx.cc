#ifndef TRANSPORT_TX
#define TRANSPORT_TX

#include <string.h>
#include <omnetpp.h>
#include "FeedbackPkt_m.h"
#include "DataPkt_m.h"
#include <vector>

using namespace omnetpp;

class TransportTx : public cSimpleModule
{
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    cOutVector bufferSizeVector;
    simtime_t serviceTime;
    simtime_t timeStampMean;
    float delay;
    float delayFlujo;
    float delayCongestion;
    uint countTimeStamp;

public:
    TransportTx();
    virtual ~TransportTx();

protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);

private:
    virtual void handleFeedback(FeedbackPkt *msg);
    virtual void handleDataPkt(cMessage *msg);
    virtual void handleEndServiceEvent();
};

Define_Module(TransportTx);

TransportTx::TransportTx()
{
    endServiceEvent = NULL;
}

TransportTx::~TransportTx()
{
    cancelAndDelete(endServiceEvent);
}

void TransportTx::initialize()
{
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    bufferSizeVector.setName("buffer size");
    delay = 0;
    delayFlujo = 0;
    delayCongestion = 0;
    serviceTime = 0.1;
    timeStampMean = 0;
    countTimeStamp = 0;
}

void TransportTx::finish()
{
}

void TransportTx::handleEndServiceEvent()
{
    if (!buffer.isEmpty())
    {

        DataPkt *pkt = dynamic_cast<DataPkt *>(buffer.pop());
        pkt->setTimeStampTx(simTime());

        send(pkt, "toOut$o");

        serviceTime += serviceTime * delay;

        if (serviceTime < pkt->getDuration())
        {
            serviceTime = pkt->getDuration();
        }

        EV << "serviceTime: " << serviceTime << "\n";
        scheduleAt(simTime() + serviceTime, endServiceEvent);
    }
}

void TransportTx::handleDataPkt(cMessage *msg)
{
    DataPkt *pkt = dynamic_cast<DataPkt *>(msg);
    if (pkt == nullptr)
    {
        delete msg;
        return;
    }

    if (buffer.getLength() >= par("bufferSize").intValue())
    {
        delete pkt;
        this->bubble("packet dropped");
    }
    else
    {
        buffer.insert(pkt);
        bufferSizeVector.record(buffer.getLength());

        if (!endServiceEvent->isScheduled())
        {
            scheduleAt(simTime(), endServiceEvent);
        }
    }
}

void TransportTx::handleFeedback(FeedbackPkt *msg)
{
    int bufferSize = msg->getBufferSize();
    int currentBufferSize = msg->getCurrentBufferSize();
    simtime_t msgTimeStamp = msg->getTimeStampRx();

    double ratio = (double)(bufferSize - currentBufferSize) / bufferSize;

    // CONTROL DE FLUJO
    if (ratio <= 0.25)
    {
        delay = 0.1;
    }
    else if (ratio > 0.5)
    {
        delay = -0.2;
    }
    else
    {
        delay = 0;
    }
    // CONTROL DE CONGESTION
    if (countTimeStamp > 5)
    {

        if (msgTimeStamp > timeStampMean * 1.25)
        {
            delayCongestion = 0.2;
            timeStampMean = msgTimeStamp;
            countTimeStamp = 1;
        }
        else if (msgTimeStamp < timeStampMean * 0.3)
        {
            delayCongestion = -0.1;
        }
        else
        {
            delayCongestion = 0;
        }
    }
    else
    {
        delayCongestion = 0;
    }
    timeStampMean = ((timeStampMean * countTimeStamp) + msgTimeStamp) / (countTimeStamp + 1);
    countTimeStamp++;

    // delay = std::max(delayFlujo, delayCongestion);
    // delay = 0.5 * delayFlujo + 0.5 * delayCongestion;

    EV << "msgTimeStamp: " << msgTimeStamp << "\n";
    EV << "timeStampMean: " << timeStampMean << "\n";
    EV << "delay: " << delay << "\n";
    delete msg;
}

void TransportTx::handleMessage(cMessage *msg)
{
    if (msg == endServiceEvent)
    {
        handleEndServiceEvent();
    }
    else if (msg->getKind() == DATA)
    {
        handleDataPkt(msg);
    }

    else if (msg->getKind() == FEEDBACK)
    {
        handleFeedback(dynamic_cast<FeedbackPkt *>(msg));
    }
}

#endif /* TRANSPORT_TX */
