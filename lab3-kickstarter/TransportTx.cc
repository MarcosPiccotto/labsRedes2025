#ifndef TRANSPORT_TX
#define TRANSPORT_TX

#include <string.h>
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
    float delay;
    simtime_t timeStampMean;
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
    delay = 0;
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

void TransportTx::handleFeedback(FeedbackPkt* msg) {
    int bufferSize = msg->getBufferSize();
    int currentBufferSize = msg->getCurrentBufferSize();
    simtime_t msgTimeStamp = msg->getTimeStampRx();

    double ratio = (double)(bufferSize - currentBufferSize) / bufferSize;

//    if (ratio <= 0.25){
//        delay = 0.1;
//    }
//    else if (ratio > 0.5){
//        delay = -0.2;
//    }
//    else{
//        delay = 0;
//    }
    delay = 0;
    if(countTimeStamp > 5){

        if(msgTimeStamp > timeStampMean * 1.2){
            delay = 0.1;
            timeStampMean = msgTimeStamp;
            countTimeStamp = 1;
        }
        else if(msgTimeStamp < timeStampMean * 0.5){
            delay = -0.2;
        }
    }

    timeStampMean = ((timeStampMean*countTimeStamp) + msgTimeStamp) / (countTimeStamp + 1);
    countTimeStamp++;
    EV << "msgTimeStamp: "<< msgTimeStamp << "\n";
    EV << "timeStampMean: "<< timeStampMean << "\n";
    EV << "delay: "<< delay << "\n";
    delete msg;
}



#endif /* TRANSPORT_TX */
