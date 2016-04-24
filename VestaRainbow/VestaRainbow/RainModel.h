//
//  RainModel.h
//  VestaRainbow
//
//  Created by Dmitry Guglya on 2016-04-23.
//  Copyright © 2016 Dmitry Guglya. All rights reserved.
//

#ifndef RainModel_h
#define RainModel_h

#include <stdio.h>

typedef struct {
    long height;
    long level;
    long capacity;
    long visits;
    int processed;
} MapPoint;

typedef struct {
    unsigned char header[138];
    int x_size;
    int y_size;
    MapPoint** points;
} MapModel;

void read_map(const char* fname, MapModel* map_model);
void write_map(const char* finput_name, const char* foutput_name, MapModel* map_model);


void calculate_capacity(MapModel* map_model);
void process_raindrop(MapModel* map_model, int x, int y);
void remove_noise(MapModel* map_model, long visit_threshold, int length_threshold);

#endif /* RainModel_h */
