#include <iostream>
#include <fstream>
#include <cmath>
#include <stdlib.h>

#include "indri/Repository.hpp"

//typedef unsigned __int64 UINT64; 

float getTFIDF(indri::index::TermData* termData, indri::index::DocListIterator::DocumentData* doc, indri::index::Index* index){
    float TF = 0;
    float IDF = 0;
    
    TF = (float)(doc->positions.size())/(index->documentLength(doc->document));
    
    IDF = (float)log((index->documentCount())/(termData->corpus.documentCount));
    
    return TF * IDF;
}

int main(int argc, char** argv){
    
    if(argc < 2){
        std::cout << "please point out where the index is.\n";
        return -1;
    }
    indri::collection::Repository r;
    std::string indexPath = argv[1];
    std::string outputPath = "output.txt";
    std::string opVocabulary = "vocabulary.txt";
    if(argc == 3){
        outputPath = argv[2] + outputPath;
    }
    //open the output file
    ofstream out;
    ofstream outVab;
    out.open(outputPath.c_str(), ios::out);
    outVab.open(opVocabulary.c_str(), ios::out);
    //First
    //get the index from repository
    r.openRead(indexPath);
    
    indri::collection::Repository::index_state state = r.indexes();
    
    indri::index::Index* index = (*state)[0];
    indri::index::DocListFileIterator* iter = index->docListFileIterator();
    iter->startIteration();
    
    UINT64 totalDocument = index->documentCount();
    UINT64 totalTerm = index->uniqueTermCount();
    std::cout << "There are " << totalTerm << " words" << std::endl;
    outVab << totalTerm << std::endl;
    UINT64 j = 0;
    //prepare room for rows and cols' info
    out << "                                                                                     \n";
    //for each word
    while(!iter->finished()){
        //Get the word 
        indri::index::DocListFileIterator::DocListData* entry = iter->currentEntry();
        indri::index::TermData* termData = entry->termData;
	outVab << termData->term << " ";
        entry->iterator->startIteration();
        indri::index::DocListIterator::DocumentData* doc = entry->iterator->currentEntry();
        char anchor[128]; 
        int finish = 0;
        //for each document
	UINT64 i = 1;
        for(i = 1; i <= totalDocument; i++){
            sprintf(anchor, "%lu", i);
            //if ith document contains the word, calculate the tf-idf and output
            if(finish != 1 && atoi(anchor) == (int)doc->document){
                //output tf-idf
                out << " " << getTFIDF(termData, doc, index);
                entry->iterator->nextEntry();
                if(!entry->iterator->finished()){
                    doc = entry->iterator->currentEntry();
                }else{
                    finish = 1;
                }
            }else{
                out << " 0";
            }
        }
        out << std::endl;
	iter->nextEntry();
	//bad display
	++j;
	int process = (j * 100)/totalTerm;
	std::cout << "\rprocessing" << process << "%";
    }
    out.seekp(0, ios::beg);
    out << j << " " << totalDocument;
    std::cout << "\nfinish\n";
    //finish output
    delete iter;
    out.close();
    outVab.close();
    r.close();
    
    return 0;
}
