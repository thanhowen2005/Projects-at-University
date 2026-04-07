#include <conio.h>
#include <iostream>
#include <string>
#include <windows.h>
#include <time.h>
#include "MENU.h"
#include "GRAPHICS.h"

char** gen2d(int p, int q);
void print2d(char** a, int p, int q, int mode, int IndexBackground);

bool IMatch(char** a, int posRow1, int posCol1, int posRow2, int posCol2);
bool LMatch(char** a, int posRow1, int posCol1, int posRow2, int posCol2);
bool ZMatch(char** a, int posRow1, int posCol1, int posRow2, int posCol2);
bool UMatch(char** a, int p, int q, int posRow1, int posCol1, int posRow2, int posCol2);
bool lineCheck(char** a, int posRow1, int posCol1, int posRow2, int posCol2);
bool checkAll(char** a, int p, int q, int posRow1, int posCol1, int posRow2, int posCol2);

int countNumOfEles(char** a, int p, int q);
void resetEle(char** a, int p, int q, int posRow1, int posCol1, int posRow2, int posCol2, int choice);
bool checkExistPair(char** a, int p, int q);
void randomAgain(char** a, int p, int q);
void moveUp(char** a, int p, int q, int& x, int& y);
void moveDown(char** a, int p, int q, int& x, int& y);
void moveLeft(char** a, int p, int q, int& x, int& y);
void moveRight(char** a, int p, int q, int& x, int& y);
void randomPos(char** a, int p, int q, int& x, int& y);