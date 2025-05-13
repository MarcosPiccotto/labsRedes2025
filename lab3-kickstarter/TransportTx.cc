#ifndef TRANSPORT_TX
#define TRANSPORT_TX

#include <string.h>
#include <algorithm>
#include <omnetpp.h>
#include "FeedbackPkt_m.h"
#include "DataPkt_m.h"
#include <vector>

using namespace omnetpp;

class TransportTx: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector delayPkt;
    float delay;
    bool flag;
    simtime_t timeStampMean;
    unsigned int countTimeStamp;

public:
    TransportTx();
    virtual ~TransportTx();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
private:
    virtual void handleFeedback(FeedbackPkt *msg);
    void flowControl(FeedbackPkt *msg);
    void congestionControl(FeedbackPkt *msg);

};

Define_Module(TransportTx);

TransportTx::TransportTx() {
    endServiceEvent = NULL;
}

TransportTx::~TransportTx() {
    cancelAndDelete(endServiceEvent);
}

void TransportTx::initialize() {
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    bufferSizeVector.setName("buffer size");
    delayPkt.setName("delay_pkt");
    delay = 0;
    flag = false;
    serviceTime = 0.1;
    timeStampMean = 0;
    countTimeStamp = 0;

}

void TransportTx::finish() {
}

void TransportTx::handleMessage(cMessage* msg) {
    if (msg == endServiceEvent) {
        if (!buffer.isEmpty()) {

            DataPkt* pkt = dynamic_cast<DataPkt*>(buffer.pop());
            pkt->setTimeStampTx(simTime());

            send(pkt, "toOut$o");

            serviceTime += serviceTime * delay;

            if (serviceTime < pkt->getDuration()) {
                serviceTime = pkt->getDuration();
            }

            EV << "serviceTime: " << serviceTime << "\n";
            scheduleAt(simTime() + serviceTime, endServiceEvent);

        }
    }
    else if (msg->getKind() == 0) {
        DataPkt* pkt = dynamic_cast<DataPkt*>(msg);
        if (pkt == nullptr) {
            delete msg;
            return;
        }

        if (buffer.getLength() >= par("bufferSize").intValue()) {
            delete pkt;
            this->bubble("packet dropped");
        } else {
            buffer.insert(pkt);
            bufferSizeVector.record(buffer.getLength());

            if (!endServiceEvent->isScheduled()) {
                scheduleAt(simTime(), endServiceEvent);
            }
        }
    }

    else if (msg->getKind() == 2) {
        handleFeedback(dynamic_cast<FeedbackPkt*>(msg));
    }
}

void TransportTx::flowControl(FeedbackPkt* msg) {
    int bufferSize = msg->getBufferSize();
    int currentBufferSize = msg->getCurrentBufferSize();

    double ratio = (double)(bufferSize - currentBufferSize) / bufferSize;

    if (ratio <= 0.25) {
        delay = 0.1;
    }
    else if (ratio > 0.5) {
        delay = -0.2;
    }
    else {
        delay = 0;
    }
}

void TransportTx::congestionControl(FeedbackPkt* msg) {
    simtime_t msgTimeStamp = msg->getTimeStampRx();

    delay = 0;

    if(countTimeStamp > 10 || flag){
        if(msgTimeStamp > timeStampMean * 1.2){
            delay = 0.2;
            timeStampMean = msgTimeStamp;
            countTimeStamp = 1;
        }
        else if(msgTimeStamp < timeStampMean * 0.2){
            delay = -0.1;
        }
        flag = true;
    }

    timeStampMean = ((timeStampMean * countTimeStamp) + msgTimeStamp) / (countTimeStamp + 1);
    countTimeStamp++;

    delayPkt.record(msgTimeStamp);
}


void TransportTx::handleFeedback(FeedbackPkt* msg) {

    // Ya que no pudimos implementar los dos al mismo tiempo
    // en esta parte se elige cuál control usar.

    // flowControl(msg);
    congestionControl(msg);

    delete msg;
}



#endif /* TRANSPORT_TX */
