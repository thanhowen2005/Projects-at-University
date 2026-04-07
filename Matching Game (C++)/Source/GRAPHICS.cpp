#include "GRAPHICS.h"

// use to change the size of terminal when running-time
void resizeConsole(int width, int height)
{
	HWND console = GetConsoleWindow();
	RECT r;
	GetWindowRect(console, &r);
	MoveWindow(console, r.left, r.top, width, height, TRUE);
}

// move the pointer to x y coordinates in terminal
void gotoxy(short x, short y) {
	HANDLE hConsoleOutput;
	COORD Cursor_an_Pos = { x - 1, y - 1 };
	hConsoleOutput = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleCursorPosition(hConsoleOutput, Cursor_an_Pos);
}

// set the color of the printed value
void setColor(int color)
{
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleTextAttribute(hConsole, color);
}


void thanhSang(int x, int y, int w, int h, int b_color, char value, int mode) {
	// mode Hidden
	if (mode == 1)
	{    // b_color is the color of the box
		if (b_color == 255)  
			b_color = 14;  // color of the current box
		if (b_color == 0)
			b_color = 8; // color of the previous box
		if (b_color == 166)
			b_color = 10; // color of choosen box
		box(x, y, h, w, ' ', mode, b_color);
	}

	// mode Normal
	else { 
		setColor(b_color); // color of the pointer when moving aroung the matrix
		for (int i = x + 1; i < x + w; i++)
		{
			for (int j = y + 1; j < y + h; j++)
			{
				gotoxy(i, j);
				cout << " ";
			}
		}
	}

	// color of the value inside the box
	if (value == ' ')
		return;

	//NORMAL Mode
	if (mode == 0)
	{
		setColor((value - '0') % 6 + 10);
		gotoxy(x + w / 2, y + h / 2);
		cout << value;
	}
	else // HIDDEN Mode
	{ 
		if (b_color == 8)
			setColor(0);// color of the previous value
		else
			setColor((value - '0') % 6 + 10); // color of the current value

		gotoxy(x + w / 2, y + h / 2);
		cout << value;
	}

	setColor((value - '0') % 6 + 10);
}

// use to draw the box in each element of the matrix of gamePlay
void box(int x, int y, int  height, int width, char value, int mode, int colorBox) {
	for (int i = x; i < x + width; i++)
		for (int j = y; j < y + height; j++)
		{
			setColor(colorBox);
			gotoxy(i, j);
			cout << " ";
		}
	//setColor(1);
	setColor(colorBox);
	for (int i = x + 1; i < x + width; i++)
	{
		gotoxy(i, y);
		cout << "-";
		gotoxy(i, y + height);
		cout << "-";
	}
	gotoxy(x, y); cout << "+";
	gotoxy(x + width, y); cout << "+";
	gotoxy(x, y + height); cout << "+";
	gotoxy(x + width, y + height); cout << "+";
	for (int i = y + 1; i < y + height; i++)
	{
		gotoxy(x, i);
		cout << char(124);
		gotoxy(x + width, i);
		cout << char(124);
	}
	if (mode == 1)
	{
		setColor(0);
		gotoxy(x + width / 2, y + height / 2);
		cout << value;
	}
	else
	{
		setColor((value - '0') % 6 + 10);
		gotoxy(x + width / 2, y + height / 2);
		cout << value;
	}
}

void ShowCur(bool CursorVisibility)
{
	HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_CURSOR_INFO cursor = { 1, CursorVisibility };
	SetConsoleCursorInfo(handle, &cursor);
}

// draw frame of chooses in LOGIN and MENU
void box2(int x, int y,int width, int height, int color, string value) {
	setColor(color);
	for (int i = x; i <= x + width ; i++)
	{
		gotoxy(i, y);
		cout << "-";
		gotoxy(i, y + height);
		cout << "-";
	}

	for (int j = y; j <= y + height; j++)
	{
		gotoxy(x, j);
		cout << char(124);
		gotoxy(x + width, j);
		cout << char(124);
	}

	gotoxy(x, y); cout << "*";
	gotoxy(x + width, y); cout << "*";
	gotoxy(x, y + height); cout << "*";
	gotoxy(x + width, y + height); cout << "*";

	gotoxy(x + 1, y + height / 2);
	cout << value;
}


// draw the sign of keyboard
void box3(int x, int y, int width, int height, string value) {
	for (int i = x; i <= x + width; i++)
	{
		gotoxy(i, y); cout << "-";
		gotoxy(i, y + height); cout << "-";
	}
	for (int j = y; j <= y + height; j++)
	{
		gotoxy(x, j); cout << char(124);
		gotoxy(x + width, j); cout << char(124);
	}

	gotoxy(x, y); cout << "+";
	gotoxy(x + width, y); cout << "+";
	gotoxy(x, y + height); cout << "+";
	gotoxy(x + width, y + height); cout << "+";
	
	gotoxy(x + 1, y + height / 2);
	cout << value;
}

// parameters and instructions when playing the game
void boardScore( int p, int q, double normalScore, double hiddenScore, int mode) {
	setColor(1);
	ifstream ifs("board.txt");
	int line = 0;
	while (!ifs.eof()) // draw frame
	{
		setColor(1);
		gotoxy((q + 3) * 8  , 2 + line);
		string s;
		getline(ifs, s, '\n');
		cout << s;
		line++;
	}

	ifs.close();
	setColor(11);
	gotoxy((q + 3) * 8 + 10, 4);
	cout << "Your highest record: ";
	setColor(9);
	if (mode == 0)
		cout << normalScore;
	else
		cout << hiddenScore;

	setColor(11);

	gotoxy((q + 3) * 8 + 10, 5);
	cout << "Current coefficient: ";
	gotoxy((q + 3) * 8 + 10, 6);
	cout << "Current score: ";

	gotoxy((q + 3) * 8 + 10, 8);
	cout << "Move: keyboard";

	box3((q + 3) * 8 + 10, 9, 6, 2, " UP");
	box3((q + 3) * 8 + 17, 9, 6, 2, "DOWN");
	box3((q + 3) * 8 + 24, 9, 6, 2,  "LEFT");
	box3((q + 3) * 8 + 31, 9, 6, 2, "RIGHT");

	gotoxy((q + 3) * 8 + 10, 13); cout << "Choose";
	box3((q + 3) * 8 + 17, 12, 8, 2, " ENTER");

	gotoxy((q + 3) * 8 + 10, 16); cout << "Hint:";
	box3((q + 3) * 8 + 15, 15, 6, 2, " TAB");

	gotoxy((q + 3) * 8 + 10, 18); cout << "Health: ";

	gotoxy((q + 3) * 8 + 10, 20);
	if (mode == 0)
		cout << "Mode: NORMAL";
	else cout << "Mode: HIDDEN";

	setColor(13);
	gotoxy((q + 3) * 8 + 10, 22); cout << "Back to menu: ";
	box3((q + 3) * 8 + 24, 21, 6, 2, " ESC");
} 

// draw background inside the matrix
void backgroundPlay(int index) {
	srand(time(NULL));
	string fileName = "play1.txtplay2.txtplay3.txtplay4.txtplay5.txtplay6.txt";
	
	ifstream ifs(fileName.substr(index, 9));
	int i = 0;
	while (!ifs.eof())
	{
		string s;
		getline(ifs, s, '\n');
		gotoxy(3, 3 + i);
		cout << s << endl;
		i++;
	}
	ifs.close();
}
