#include <conio.h>
#include <iostream>
#include <string>
#include <windows.h>
#include <time.h>
#include "MENU.h"
#include "GAME&MATCHING.h"

void play(int p, int q, int mode, int posPlayer, profile* player, int numOfPlayer, double tempPoint, double coefficient, int stage);
void hint(char** a, int p, int q, int mode);
void saveRecords(profile* player, int numOfPlayer, int posPlayer, double tempPoint, int mode, int stage);
void winGame(int numOfCols, profile* player, int numOfPlayer, int posPlayer);
void failGame(int numOfCols, profile* player, int numOfPlayer, int posPlayer);
