#include <iostream>
#include <fstream>
#include "LOGIN.h"
#include "MENU.h"
#include <thread>
#include "GRAPHICS.h"
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

using namespace std;
// game will start with help() to help you know how to use play game
int main() {
	PlaySound(TEXT("GameStartMusic.wav"), NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);
	help();
}