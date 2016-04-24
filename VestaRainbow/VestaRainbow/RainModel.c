//
//  RainModel.c
//  VestaRainbow
//
//  Created by Dmitry Guglya on 2016-04-23.
//  Copyright © 2016 Dmitry Guglya. All rights reserved.
//

#include "RainModel.h"
#include <limits.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int x, y;
} XY;

void free_map_points(MapModel* map_model)
{
    if (map_model->points == NULL) return;
    
    for (int x = 0; x < map_model->x_size; x++) {
        free(map_model->points[x]);
    }
}

void allocate_map_points(MapModel* map_model, int x, int y)
{
    if (map_model->points) free_map_points(map_model);
    
    map_model->x_size = x;
    map_model->y_size = y;
    map_model->points = malloc(sizeof(MapPoint*)*map_model->x_size);
    for (int x = 0; x < map_model->x_size; x++) {
        map_model->points[x] = malloc(sizeof(MapPoint)*map_model->y_size);
    }
}

void read_map(const char* fname, MapModel* map_model)
{
    int i;
    FILE* f = fopen(fname, "rb");
    unsigned char info[138];
    
    fread(info, sizeof(unsigned char), 138, f);
    
    // extract image height and width from header
    int width = *(int*)&info[18];
    int height = *(int*)&info[22];
    
    int size = 4 * width * height;
    unsigned char* data = malloc(size);
    fread(data, sizeof(unsigned char), size, f); 
    fclose(f);
    
    allocate_map_points(map_model, width, height);
    
    for(i = 0; i < size; i += 4) {
        int x = (i / 4) % width;
        int y = (i / 4) / width;
        map_model->points[x][y].height = data[i];
    }
    
    free(data);
}

void calculate_capacity(MapModel* map_model)
{
    int capacity_distribution[256];
    memset(capacity_distribution, 0, sizeof(capacity_distribution));
    
    for (int x = 0; x < map_model->x_size; x++) {
        for (int y = 0; y < map_model->y_size; y++) {
            long min_height = LONG_MAX;
            for (int dx = -1; dx <= 1; dx++) {
                for (int dy = -1; dy <= 1; dy++) {
                    if (dx == 0 && dy == 0) continue;
                    if ((x + dx) < 0 || (y + dy) < 0) continue;
                    if ((x + dx) >= map_model->x_size || (y + dy) >= map_model->y_size ) continue;

                    if (map_model->points[x][y].height >= map_model->points[x+dx][y+dy].height) {
                        goto no_capacity;
                    
                    }
                    if (map_model->points[x+dx][y+dy].height < min_height)
                        min_height = map_model->points[x+dx][y+dy].height;
                }
            }
            
            map_model->points[x][y].capacity = min_height - map_model->points[x][y].height;
            
            capacity_distribution[map_model->points[x][y].capacity]++;
            
        no_capacity: continue;
        }
    }

    for (int i = 0; i < 256; i++) {
        if (capacity_distribution[i] != 0) {
            printf("Capacity %d count %d\n", i, capacity_distribution[i]);
        }
    }
}

void recalculate_capacity(MapModel* map_model, int x, int y)
{
    
}


void process_raindrop(MapModel* map_model, int x, int y)
{
    long min_height = LONG_MAX;
    int step;
    XY next_points[9], same_height_points[1000];
    int next_point_count, next_point = 0;
    int same_height_point_count;
    
    same_height_point_count = 0;
    for (step = 0; step < 1000; step++) {
        map_model->points[x][y].visits++;
        
        next_point_count = 0;
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                // On the map
                if (dx == 0 && dy == 0) continue;
                if ((x + dx) < 0 || (y + dy) < 0) continue;
                if ((x + dx) >= map_model->x_size || (y + dy) >= map_model->y_size ) continue;
                
                // Going downhill
                if (map_model->points[x][y].height < map_model->points[x+dx][y+dy].height) continue;
                
                // Where to go
                if (map_model->points[x+dx][y+dy].height < min_height) {
                    next_points[0].x = x+dx;
                    next_points[0].y = y+dy;
                    next_point_count = 1;
                    min_height = map_model->points[x+dx][y+dy].height;
                }
                else if (map_model->points[x+dx][y+dy].height == min_height) {
                    next_points[next_point_count].x = x+dx;
                    next_points[next_point_count].y = y+dy;
                    next_point_count++;
                }
            }
        }
        
        if (next_point_count == 0) {
            map_model->points[x][y].height++;
            break;
        }
        
        while (next_point_count > 0) {
            next_point = rand() % next_point_count;
            
            // On the slope - break
            if (map_model->points[x][y].height > min_height) {
                same_height_point_count = 0;
                break;
                
            }
            
            // First time on even surface - save and break
            if (same_height_point_count == 0) {
                same_height_points[0].x = x;
                same_height_points[0].y = y;
                same_height_point_count++;
                break;
            }

            // Check all same plane elements
            int i;
            for (i = 0; i < same_height_point_count; i++) {
                if ((same_height_points[i].x == next_points[next_point].x) &&
                    (same_height_points[i].y == next_points[next_point].x)) {
                    
                    next_point_count--;
                    next_points[next_point] = next_points[next_point_count];
                    break;
                }
            }
            
            // Not found - break
            if (i == same_height_point_count)
                break;

        }
        
        if (next_point_count == 0) {
            break;
        }
        
        x = next_points[next_point].x;
        y = next_points[next_point].y;
    }
}

void add_neighbours(MapModel* map_model, int x, int y, XY* neighbours, int* count, int limit, long visits)
{
    if (*count >= limit)
        return;

    if (map_model->points[x][y].visits < visits)
        return;

    for (int i = 0; i < (*count); i++) {
        if (neighbours[i].x == x && neighbours[i].y == y) {
            return;
        }
    }
    
    neighbours[*count].x = x;
    neighbours[*count].y = y;
    *count += 1;
    
    for (int dx = -1; dx <= 1; dx++) {
        for (int dy = -1; dy <= 1; dy++) {
            if (dx == 0 && dy == 0) continue;
            if ((x + dx) < 0 || (y + dy) < 0) continue;
            if ((x + dx) >= map_model->x_size || (y + dy) >= map_model->y_size ) continue;
            add_neighbours(map_model, x + dx, y + dy, neighbours, count, limit, visits);
        }
    }
}

void remove_noise(MapModel* map_model, long visit_threshold, int length_threshold)
{
    XY* neighbours = malloc(sizeof(XY)*length_threshold);
    int neighbours_count = 0;

    for (int x = 0; x < map_model->x_size; x++) {
        for (int y = 0; y < map_model->y_size; y++) {
            map_model->points[x][y].processed = 0;
        }
    }
    
    for (int x = 0; x < map_model->x_size; x++) {
        for (int y = 0; y < map_model->y_size; y++) {
            if (map_model->points[x][y].visits < visit_threshold) {
                map_model->points[x][y].visits = 0;
                continue;
            }
            if (map_model->points[x][y].processed != 0)
                continue;
            
            neighbours_count = 0;
            add_neighbours(map_model, x, y, neighbours, &neighbours_count, length_threshold, visit_threshold);

            if (neighbours_count < length_threshold) {
                for (int i = 0; i < neighbours_count; i++) {
                    map_model->points[neighbours[i].x][neighbours[i].y].visits = 0;
                }
            }
            else {
                for (int i = 0; i < neighbours_count; i++) {
                    map_model->points[neighbours[i].x][neighbours[i].y].processed = 1;
                }
            }
        }
    }
    
    
}

void write_map(const char* finput_name, const char*foutput_name, MapModel* map_model)
{
    int i;
    
    // BMP image write should be re-written - we do not have enough time for that
    FILE* f = fopen(finput_name, "rb");
    unsigned char info[138];
    fread(info, sizeof(unsigned char), 138, f);
    
    // extract image height and width from header
    int width = *(int*)&info[18];
    int height = *(int*)&info[22];
 
    int size = 4 * width * height;
    unsigned char* data = malloc(size);

    fclose(f);
    
    f = fopen(foutput_name, "wb");
    fwrite(info, sizeof(unsigned char), 138, f);
    
    
    // Actual data
    i = 0;
    for (int y = 0; y < map_model->y_size; y++) {
        for (int x = 0; x < map_model->x_size; x++) {
            data[i] = (unsigned char)(map_model->points[x][y].visits & 0xFF);
            data[i+1] = 0;
            data[i+2] = 0;
            data[i+3] = map_model->points[x][y].visits > 0 ? 0xFF : 0;
            i += 4;
        }
    }

    fwrite(data, sizeof(unsigned char), size, f); // read the rest of the data at once
    fclose(f);
        
    free(data);
}