//
//  main.m
//  VestaRainbow
//
//  Created by Dmitry Guglya on 2016-04-23.
//  Copyright © 2016 Dmitry Guglya. All rights reserved.
//

#include "RainModel.h"
#include <string.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, const char * argv[]) {
    
    if (argc != 6) {
        printf("Usage: neomapper <source_file> <N> <V> <S> <output_file>\n");
        printf("       N - number of raindrops\n");
        printf("       V - number of visits threshold\n");
        printf("       S - size threshold\n");
        exit(0);
    }
    
    long drops_count = atol(argv[2]);
    long v = atol(argv[3]);
    int s = atoi(argv[4]);
    
    srand((unsigned int)time(NULL));
    
    MapModel map_model;
    memset(&map_model, 0, sizeof(map_model));
    
    read_map(argv[1], &map_model);
    calculate_capacity(&map_model);
    
    for (long n = 0; n < drops_count; n++) {
        process_raindrop(&map_model, arc4random_uniform(map_model.x_size), arc4random_uniform(map_model.y_size));
        if ((n % 100000) == 0) printf("time %ld processed %ld drops\n", time(NULL), n);
    }
    
    remove_noise(&map_model, v, s);
    write_map(argv[1], argv[5], &map_model);

    return 0;
}
