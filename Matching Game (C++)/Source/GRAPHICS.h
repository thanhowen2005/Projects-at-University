#include <iostream>
#include <fstream>
#include <windows.h>
#include <thread>
#include <string>
#include <string.h>
#include <time.h>
#include <stdlib.h>

#define UP 72
#define DOWN 80
#define LEFT 75
#define RIGHT 77
#define ENTER 13
#define HINT 9
#define ESC 27

using namespace std;

void gotoxy(short x, short y);
void setColor(int color);
void thanhSang(int x, int y, int w, int h, int b_color, char value, int mode);
void box(int x, int y, int  height, int width, char value, int mode, int colorBox);
void resizeConsole(int width, int height);
void ShowCur(bool CursorVisibility);
void box2(int x, int y, int width, int height, int color, string value);
void boardScore(int p, int q, double normalScore, double hiddenScore, int mode);
void box3(int x, int y, int width, int height, string value);
void backgroundPlay(int index);