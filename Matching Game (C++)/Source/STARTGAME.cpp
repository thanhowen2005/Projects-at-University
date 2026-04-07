#include "STARTGAME.h"
#include "GRAPHICS.h"
#include "MENU.h"
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

using namespace std;

// saves the player's score after completing a game
void saveRecords(profile* player, int numOfPlayer, int posPlayer, double tempPoint, int mode, int stage){
	if (stage != 0 && tempPoint > player[posPlayer].stepScore)
		player[posPlayer].stepScore = tempPoint;
	if (tempPoint > player[posPlayer].normalScore && mode == 0 && stage == 0)
		player[posPlayer].normalScore = tempPoint;
	
	if (tempPoint > player[posPlayer].hiddenScore && mode == 1 && stage == 0)
		player[posPlayer].hiddenScore = tempPoint;
	ofstream ofs("records.txt");
	for (int i = 0; i < numOfPlayer; i++)
	{ 
		ofs << player[i].username << " " << player[i].password << " " << player[i].normalScore << " " << player[i].hiddenScore << " " << player[i].stepScore << "\n";
	}
	ofs.close();
}

// move suggestion in game play
void hint(char** a, int p, int q, int mode) {
	srand(time(NULL));
	int posRow1 = 0, posCol1 = 0, posRow2 = 0, posCol2 = 0;
	for (int i = 0; i < p; i++)
		for (int j = 0; j < q; j++)
			for (int k = i; k < p; k++)
				for (int l = j; l < q; l++)
					if (checkAll(a, p, q, i, j, k, l) && a[i][j] != ' ' && a[k][l] != ' ')
					{
						posRow1 = i;
						posCol1 = j;
						posRow2 = k;
						posCol2 = l;
					}
	thanhSang(2 + posCol1 * 8, 2 + posRow1 * 4, 8, 4, 220, a[posRow1][posCol1], mode);
	thanhSang(2 + posCol2 * 8, 2 + posRow2 * 4, 8, 4, 220, a[posRow2][posCol2], mode);
	this_thread::sleep_for(chrono::seconds(1));
	thanhSang(2 + posCol1 * 8, 2 + posRow1 * 4, 8, 4, 0, a[posRow1][posCol1], mode);
	thanhSang(2 + posCol2 * 8, 2 + posRow2 * 4, 8, 4, 0, a[posRow2][posCol2], mode);
}


// play game
void play(int p, int q, int mode, int posPlayer, profile* player, int numOfPlayer, double tempPoint, double coefficient, int stage) {

	resizeConsole(1600, 900);
	system("cls");
	PlaySoundA(NULL, NULL, SND_FILENAME);
	ShowCur(0);

	//double tempPoint = 0;
	//double coefficient = 1;

	int health = 3;
	int numOfHints = (p + q) / 2;

	int numOfPairs = p * q / 2;

	char** a = gen2d(p, q);
	int x = 0, y = 0;
	int xcu = x, ycu = y;
	int count = 0;
	int row1 = -1, col1 = -1, row2 = -1, col2 = -1;
	
	// random background in gameplay
	int index;
	string fileName = "play1.txtplay2.txtplay3.txtplay4.txtplay5.txtplay6.txt";
	if (q < 5)
		index = (rand() % 2) * 9;
	else
		if (q == 6)
			index = (rand() % 2 + 2) * 9;
		else
			index = (rand() % 2 + 4) * 9;
	backgroundPlay(index);

	// print gameplay
	print2d(a, p, q, mode, index);
	boardScore(p, q, player[posPlayer].normalScore, player[posPlayer].hiddenScore, mode);
	setColor(6);
	gotoxy((q + 3) * 8 + 30, 5); cout << coefficient;
	gotoxy((q + 3) * 8 + 25, 6); cout << tempPoint << "     ";
	gotoxy((q + 3) * 8 + 23, 16); cout << numOfHints;
	gotoxy((q + 3) * 8 + 17, 18); cout << health;
	
	int c = 0;
	while (true)
	{
		
		if (!checkExistPair(a, p, q)) {
			randomAgain(a, p, q);
			backgroundPlay(index);
			print2d(a, p, q, mode, index);

			setColor(6);
			gotoxy((q + 3) * 8 + 30, 5); cout << coefficient;
			gotoxy((q + 3) * 8 + 25, 6); cout << tempPoint << "   ";
			gotoxy((q + 3) * 8 + 23, 16); cout << numOfHints;
			gotoxy((q + 3) * 8 + 17, 18); cout << health;
		}

		if (a[xcu][ycu] != ' ') {
			thanhSang(2 + ycu * 8, 2 + xcu * 4, 8, 4, 8, a[xcu][ycu], mode);
		}
		if (count == 1) {
			thanhSang(2 + col1 * 8, 2 + row1 * 4, 8, 4, 166, a[row1][col1], mode);
		}

		thanhSang(2 + y * 8, 2 + x * 4, 8, 4, 255, a[x][y], mode);
		xcu = x; ycu = y;


			switch (c = _getch()) {
			case UP:
					PlaySound(TEXT("Navigation.wav"), NULL, SND_FILENAME | SND_ASYNC);
					moveUp(a, p, q, x, y);
				break;
			case DOWN:
					PlaySound(TEXT("Navigation.wav"), NULL, SND_FILENAME | SND_ASYNC);
					moveDown(a, p, q, x, y);
				break;
			case LEFT:
					PlaySound(TEXT("Navigation.wav"), NULL, SND_FILENAME | SND_ASYNC);
					moveLeft(a, p, q, x, y);
				break;
			case RIGHT:
					PlaySound(TEXT("Navigation.wav"), NULL, SND_FILENAME | SND_ASYNC);
					moveRight(a, p, q, x, y);
				break;
			case ENTER:
				count++;
				if (count == 1) {
					PlaySound(TEXT("Enter.wav"), NULL, SND_FILENAME | SND_ASYNC);
					row1 = x;
					col1 = y;

				}
				if (count == 2)
				{
					if (x == row1 && y == col1)
					{
						PlaySound(TEXT("Enter.wav"), NULL, SND_FILENAME | SND_ASYNC);
						thanhSang(2 + col1 * 8, 2 + row1 * 4, 8, 4, 0, a[row1][col1], mode);
						count -= 2;
					}
					else {
						row2 = x;
						col2 = y;
						if (!checkAll(a, p, q, row1, col1, row2, col2)) {
							health--;
							coefficient = 1;
							if (tempPoint >= 5)
								tempPoint -= 5;
							setColor(6);
							gotoxy((q + 3) * 8 + 25, 6); cout << tempPoint << "   ";
							gotoxy((q + 3) * 8 + 30, 5); cout << coefficient << "  ";
							gotoxy((q + 3) * 8 + 17, 18); cout << health;

							PlaySound(TEXT("WrongMatch.wav"), NULL, SND_FILENAME | SND_ASYNC);
							thanhSang(2 + col1 * 8, 2 + row1 * 4, 8, 4, 200, a[row1][col1], mode);
							thanhSang(2 + col2 * 8, 2 + row2 * 4, 8, 4, 200, a[row2][col2], mode);
							this_thread::sleep_for(chrono::milliseconds(250));
							thanhSang(2 + col1 * 8, 2 + row1 * 4, 8, 4, 0, a[row1][col1],  mode);
							thanhSang(2 + col2 * 8, 2 + row2 * 4, 8, 4, 0, a[row2][col2], mode);
							row1 = row2 = col1 = col2 = -1;
							count = 0;
						}
						else {
							tempPoint += 5 * coefficient;
							coefficient += 0.1;

							PlaySound(TEXT("CorrectMatch.wav"), NULL, SND_FILENAME | SND_ASYNC);

							thanhSang(2 + col2 * 8, 2 + row2 * 4, 8, 4, 166, a[row2][col2], mode);
							this_thread::sleep_for(chrono::milliseconds(250));
							resetEle(a, p, q, row1, col1, row2, col2, mode);

							box(2 + col1 * 8, 2 + row1 * 4, 4, 8, a[row1][col1], mode, 0);
							box(2 + col2 * 8, 2 + row2 * 4, 4, 8, a[row2][col2], mode, 0);
							
							print2d(a, p, q, mode, index);
							//boardScore(p, q, player[posPlayer].normalScore, player[posPlayer].hiddenScore, mode);
							setColor(6);
							gotoxy((q + 3) * 8 + 25, 6); cout << tempPoint << "   ";
							gotoxy((q + 3) * 8 + 30, 5); cout << coefficient;
							gotoxy((q + 3) * 8 + 23, 16); cout << numOfHints;
							gotoxy((q + 3) * 8 + 17, 18); cout << health;

							row1 = row2 = col1 = col2 = -1;
							count = 0;
							numOfPairs--;
							if (numOfPairs != 0)
								randomPos(a, p, q, x, y);
						}
					}
				}
				break;
			case HINT:
				if (numOfHints != 0) {
					PlaySound(TEXT("Hint.wav"), NULL, SND_FILENAME | SND_ASYNC);
					hint(a, p, q, mode);

					numOfHints--;
					if (tempPoint >= 5)
						tempPoint -= 5;

					setColor(6);
					gotoxy((q + 3) * 8 + 25, 6); cout << tempPoint << "   ";
					gotoxy((q + 3) * 8 + 23, 16); cout << numOfHints <<"  ";
				}
				break;
			case ESC:
				PlaySound(TEXT("GameStartMusic"), NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);
				system("cls");
				menu(posPlayer);
			}
		
		if (health == 0) {
			saveRecords(player, numOfPlayer, posPlayer, tempPoint, mode, stage);
			failGame(q, player, numOfPlayer, posPlayer);
			break;
		}
		if (numOfPairs == 0) {
			saveRecords(player, numOfPlayer, posPlayer, tempPoint, mode, stage);
			if (stage == 1)
			{
				stage++;
				system("cls");
				cout << "NEXT STAGE....";
				this_thread::sleep_for(chrono::milliseconds(1500));
				play(6, 6, 0, posPlayer, player, numOfPlayer, tempPoint, coefficient, stage);
			}

			if (stage == 2)
			{
				system("cls");
				cout << "NEXT STAGE....";
				this_thread::sleep_for(chrono::milliseconds(1500));
				stage++;
				play(8, 8, 0, posPlayer, player, numOfPlayer, tempPoint, coefficient, stage);
			}

			if (stage == 3)
			{
				system("cls");
				cout << "NEXT STAGE....";
				this_thread::sleep_for(chrono::milliseconds(1500));
				stage++;
				play(4, 4, 1, posPlayer, player, numOfPlayer, tempPoint, coefficient, stage);
			}

			if (stage == 4)
			{
				system("cls");
				cout << "NEXT STAGE....";
				this_thread::sleep_for(chrono::milliseconds(1500));
				stage++;
				play(6, 6, 1, posPlayer, player, numOfPlayer, tempPoint, coefficient, stage);
			}

			winGame(q, player, numOfPlayer, posPlayer);
			break;
		}
	}
}


// background after wining 
void winGame(int numOfCols, profile *player, int numOfPlayer, int posPlayer) {
	ifstream read("win.txt");
	int i = 28;
	while (!read.eof())
	{
		string s;
		getline(read,s, '\n');
		
		gotoxy((numOfCols + 3) * 8 + 7, i++);
		cout << s;
	}
	read.close();
	
	PlaySound(TEXT("WinGame.wav"), NULL, SND_FILENAME);

	setColor(4);
	gotoxy((numOfCols + 3) * 8 + 7, i + 2);
	cout << "\tPress ESC to back to Menu";
	int c = _getch();
	while (c != ESC)
	{
		c = _getch();
	}

	PlaySound(TEXT("GameStartMusic.wav"), NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);
	
	system("cls");
	menu(posPlayer);
}

//background after losing
void failGame(int numOfCols, profile* player, int numOfPlayer, int posPlayer) {
	system("cls");
	ifstream read("defeat.txt");
	int i = 10;

	while (!read.eof())
	{
		gotoxy(20, i++);
		string s;
		getline(read, s, '\n');
		cout << s;
	}
	read.close();

	PlaySound(TEXT("GameOver.wav"), NULL, SND_FILENAME);

	setColor(4);
	gotoxy(60, i + 2);
	cout << "\tPress ESC to back to Menu";
	int c = _getch();
	while (c != ESC)
	{
		c = _getch();
	}

	PlaySound(TEXT("GameStartMusic.wav"), NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);

	system("cls");
	menu(posPlayer);

}

