enum typePkt {
    DATA = 0;
    FEEDBACK = 2;
}

packet FeedbackPkt {
    int currentBufferSize;
    int bufferSize; 
    simtime_t timeStampRx;
}

