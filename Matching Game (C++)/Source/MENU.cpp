#include "MENU.h"
#include "GRAPHICS.h"
#include "LOGIN.h"
#include "STARTGAME.h"
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

using namespace std;

//introduce information about project
void introduction(int posPlayer) {
	system("cls");
	ifstream read("Introduction.txt");
	int i = 1;
	while (!read.eof())
	{
		
		setColor(11);
		if (i <= 8)
			setColor(14);
		string s;
		getline(read, s, '\n');

		gotoxy(20, 1 + i);
		cout << s << endl;
		i++;
	}
	read.close();

	gotoxy(54, 10);
	setColor(14); cout << "MATCHING GAME";

	gotoxy(48, i - 3);
	setColor(14); cout << " UNIVERSITY OF SCIENCE ";
	gotoxy(56, i - 2);
	setColor(14); cout << "23CLC10";

	setColor(4);
	gotoxy(47, 1 + i + 1); cout << "Press ESC to back to Menu";
	int c;
	do {
		c = _getch();
	} while (c != ESC);
	system("cls");
	menu(posPlayer);


}

// Show scores for each mode and scores are arranged in order from high to low
void leaderboard(profile* player, int numOfPlayer, int posPlayer) {
	ShowCur(0);
	ifstream ifs("leaderboard.txt");
	int i = 0;
	while (!ifs.eof())
	{
		gotoxy(25, 3 + i);
		setColor(10);
		string s;
		getline(ifs, s, '\n');
		cout << s << endl;
		i++;
	}
	ifs.close();
	gotoxy(12, 3 + i); cout << "PLAYER";
	gotoxy(30, 3 + i); cout << "NORMAL MODE";
	gotoxy(48, 3 + i); cout << "PLAYER";
	gotoxy(66, 3 + i); cout << "HIDDEN MODE";
	gotoxy(84, 3 + i); cout << "PLAYER";
	gotoxy(102, 3 + i); cout << "STEP BY STEP MODE";

	// generate new array to sort and displace
	profile* playerCoppy = new profile[numOfPlayer];
	for (int i = 0; i < numOfPlayer; i++)
		playerCoppy[i] = player[i];


	//The wall between the scoreboards
	for (int i = 0; i <= numOfPlayer; i++)
	{
		gotoxy(43, 9 + i);
		setColor(15);
		cout << "|";

		gotoxy(79, 9 + i);
		setColor(15);
		cout << "|";
	}


	// Sort by normal score ascending
	for (int i = 0; i < numOfPlayer - 1; i++)
		for (int j = i + 1; j < numOfPlayer; j++)
			if (playerCoppy[i].normalScore < playerCoppy[j].normalScore)
			{
				profile temp = playerCoppy[i];
				playerCoppy[i] = playerCoppy[j];
				playerCoppy[j] = temp;
			}
	// Scoreboard of normal mode
	for (int i = 0; i < numOfPlayer; i++)
	{	
		setColor(6);
		if (playerCoppy[i].username == player[posPlayer].username)
			setColor(4);
			
		gotoxy(12, 10 + i);
		cout << playerCoppy[i].username;
		gotoxy(30, 10 + i);
		cout << playerCoppy[i].normalScore;
	}

	// Sort by hidden score ascending
	for (int i = 0; i < numOfPlayer - 1; i++)
		for (int j = i + 1; j < numOfPlayer; j++)
			if (playerCoppy[i].hiddenScore < playerCoppy[j].hiddenScore)
			{
				profile temp = playerCoppy[i];
				playerCoppy[i] = playerCoppy[j];
				playerCoppy[j] = temp;
			}
	// Scoreboard of hidden mode
	for (int i = 0; i < numOfPlayer; i++)
	{
		setColor(6);
		if (playerCoppy[i].username == player[posPlayer].username)
			setColor(4);

		gotoxy(48, 10 + i);
		cout << playerCoppy[i].username;
		gotoxy(66, 10 + i);
		cout << playerCoppy[i].hiddenScore;
	}


	// Sort by step score ascending
	for (int i = 0; i < numOfPlayer - 1; i++)
		for (int j = i + 1; j < numOfPlayer; j++)
			if (playerCoppy[i].stepScore < playerCoppy[j].stepScore)
			{
				profile temp = playerCoppy[i];
				playerCoppy[i] = playerCoppy[j];
				playerCoppy[j] = temp;
			}
	// Scoreboard of step by step mode
	for (int i = 0; i < numOfPlayer; i++)
	{
		setColor(6);
		if (playerCoppy[i].username == player[posPlayer].username)
			setColor(4);

		gotoxy(84, 10 + i);
		cout << playerCoppy[i].username;
		gotoxy(102, 10 + i);
		cout << playerCoppy[i].stepScore;
	}


	delete[]playerCoppy;

	setColor(15);
	gotoxy(40, 10 + numOfPlayer + 4);
	cout << "Press ESC to back to the Menu";
	int press;
	do
	{
		press = _getch();
	} while (press != 27);
	system("cls");
	menu(posPlayer);
	setColor(0);
}




// MENU
void menu(int posPlayer) {
	resizeConsole(1000, 600);
	ShowCur(0); // delete sign of pointer
	int numOfPlayer = 0;

	// count the number of profiles that have been saved
	ifstream ifs0("records.txt");
	while (!ifs0.eof())
	{
		string garbage = " ";
		getline(ifs0, garbage);
		numOfPlayer++;
	}
	numOfPlayer--;
	ifs0.close();

	// Allocate  
	profile* player = new profile[numOfPlayer];


	//saved all player into struct player
	ifstream ifs1("records.txt");
	int count = 0;
	while (!ifs1.eof())
	{
		ifs1 >> player[count].username;
		ifs1 >> player[count].password;
		ifs1 >> player[count].normalScore;
		ifs1 >> player[count].hiddenScore;
		ifs1 >> player[count].stepScore;
		count++;
	}
	ifs1.close();

	// draw background at menu
	cout << "\n\n\n\n\n\n";
	ifstream ifs("background.txt");
	while (!ifs.eof())
	{
		setColor(12);
		string s;
		getline(ifs, s);
		cout << "\t" << s << endl;
	}
	ifs.close();
	setColor(15);
	string s[4] = { "  START GAME", " INTRODUCTION", "	   RANK", "BACK TO LOGIN" };
	// draw options
	box2(22, 16, 15, 2, 15, s[0]);
	box2(22 + 20, 16, 15, 2, 15, s[1]);
	box2(22 + 40, 16, 15, 2, 15, s[2]);
	box2(22 + 60, 16, 15, 2, 15, s[3]);
	
	int posMode = 0, posLevel = 0;
	int c = 0;
	int countString = 0;
	int oldString = 0;
	box2(22, 16, 15, 2, 10, s[0]);


	while (true)
	{
		box2(22 + oldString * 20, 16, 15, 2, 15, s[oldString]);
		box2(22 + countString * 20, 16, 15, 2, 10, s[countString]);
		oldString = countString;

		int option;
		switch (option = _getch())
		{
			case LEFT:
				countString--;
				if (countString == -1)
					countString = 3;
				break;
			case RIGHT:
				countString++;
				if (countString == 4)
					countString = 0;
				break;
			case ENTER: 
			{
				if (countString == 0) // option 1 : start game
				{
					system("cls");
					setColor(15);
					string mode[4] = { "NORMAL MODE","HIDDEN MODE", "STEP BY STEP","BACK TO MENU"};
					string level[3] = { "STANDARD","CUSTOM", "BACK TO MENU"};
					ShowCur(0);
					while (true) // choose mode
					{
						choose(mode, 4, posMode);
						switch (c = _getch())
						{
							case LEFT:
								if (posMode > 0)
									posMode--;
								break;
							case RIGHT:
								if (posMode < 3) 
									posMode++;
								break;
							case ENTER: {
								switch (posMode)
								{
								case 0:
									while (true) // choose level (standard or custom)
									{
										choose(level, 3, posLevel);
										switch (c = _getch())
										{
											case LEFT:
												if (posLevel > 0)
													posLevel--;
												break;
											case RIGHT:
												if (posLevel < 2)
													posLevel++;
												break;
											case ENTER:
												switch (posLevel)
												{
												case 0:
													play(6, 6, 0, posPlayer, player, numOfPlayer, 0, 1.0, 0);
													break;
												case 1:
													ShowCur(1);
													int p, q;
													setColor(13);
													cout << "Input the number of rows: ";
													cin >> p;
													cout << "Input the number of columns: ";
													cin >> q;
													while ( (p * q) % 2 != 0 || q < 4 || p < 4 || p > 10 || q > 10) {
														system("cls");
														choose(level, 3, posLevel);
														setColor(12);
														cout << "Please input the number of rows and columns that rows * columns is an even number!" << endl;
														cout << "Number of Rows and Columns must be from 4 to 10" << endl;
														setColor(13);
														cout << "Input the number of rows again: ";
														cin >> p;
														cout << "Input the number of columns again: ";
														cin >> q;
													}
													play(p, q, 0, posPlayer, player, numOfPlayer, 0, 1.0, 0);
													break;
												case 2:
													system("cls");
													menu(posPlayer);
													break;
												}
										}
									}
								case 1:
									while (true) // choose level (standard or custom)
									{
										choose(level, 3, posLevel);
										switch (c = _getch())
										{
											case LEFT:
												if (posLevel > 0)
													posLevel--;
												break;
											case RIGHT:
												if (posLevel < 2)
													posLevel++;
												break;
											case ENTER:
												switch (posLevel)
												{
												case 0:
													play(6, 6, 1, posPlayer, player, numOfPlayer, 0, 1.0, 0);
													break;
												case 1:
													ShowCur(1);
													int p, q;
													setColor(13);
													cout << "Input the number of rows: ";
													cin >> p;
													cout << "Input the number of columns: ";
													cin >> q;
													while ((p * q) % 2 != 0 || q < 4 || p < 4 || p > 10 || q > 10)
													{
														system("cls");
														choose(level, 3, posLevel);
														setColor(12);
														cout << "Please input the number of rows and columns that rows * columns is an even number!" << endl;
														cout << "Number of Rows and Columns must be from 4 to 10" << endl;
														setColor(13);
														cout << "Input the number of rows again: ";
														cin >> p;
														cout << "Input the number of columns again: ";
														cin >> q;
													}
													play(p, q, 1, posPlayer, player, numOfPlayer, 0, 1.0, 0);
													break;
												}
												case 2:
													system("cls");
													menu(posPlayer);
													break;
										}
									}
								case 2: 
									play(4, 4, 0, posPlayer, player, numOfPlayer, 0, 1.0, 1);
								case 3:
									system("cls");
									menu(posPlayer);
									break;
								}
							}
						}
					}
				}
				else if (countString == 1) { 
					introduction(posPlayer); // option2
				}
				else if (countString == 2) { 
					system("cls");
					leaderboard(player, numOfPlayer, posPlayer); // option3
				}
				else if (countString == 3) { 
					system("cls"); 
					start(); // option4 back to menu
				}
				else {
					system("cls");
					menu(posPlayer);
				}
			}
		}
	}
}


// change position of the pointer when change selection
void choose(string ans[], int n, int pos) {
	system("cls");
	cout << "\n\n\n\n";
	ifstream ifs("background.txt");
	while (!ifs.eof())
	{
		setColor(10);
		string s;
		getline(ifs, s);
		cout << "\t" << s << endl;
	}
	setColor(12);
	ifs.close();
	cout << "\t\t--------------------------------------------------------------------------------------" << endl;

	if (n == 4)
		cout << "\t\t\t";
	if (n == 3)
		cout << "\t\t\t\t";

	for (int i = 0; i < n; i++) {
		if (i == pos) {
			setColor(12);
			cout << "  <";
			setColor(11);
			cout << ans[i];
			setColor(12);
			cout << ">" << "   ";
		}
		else {
			setColor(11);
			cout << "   " << ans[i] << " " << "   ";
		}
	}
	cout << endl;
	setColor(12);
	cout << "\t\t--------------------------------------------------------------------------------------" << endl;
	ifs.open("background2.txt");
	while (!ifs.eof())
	{
		setColor(10);
		string s;
		getline(ifs, s);
		cout << "\t" << s << endl;
	}
	ifs.close();
}

