#include "GAME&MATCHING.h"

// use to count the number of remaining cells that have not been matched 
int countNumOfEles(char** a, int p, int q) {
	int count = 0;
	for (int i = 0; i < p; i++)
		for (int j = 0; j < q; j++)
			if (a[i][j] != ' ')
				count++;
	return count;
}


// create random value in each in size of matrix 
void randomAgain(char** a, int p, int q) {
	srand(time(NULL));
	int amount = countNumOfEles(a, p, q) / 2;

	if (amount > 26)
		amount = 26;

	for (int i = 0; i < p; i++) {
		for (int j = 0; j < q; j++) {
			if (a[i][j] != ' ') {
				a[i][j] = 65 + rand() % amount;
			}
		}
	}
}

// create new matrix when starting game
char** gen2d(int p, int q) {
	srand(time(NULL));
	char** a = new char* [p];
	for (int i = 0; i < p; i++) {
		a[i] = new char[q];
	}
	randomAgain(a, p, q);
	return a;
}

// use to print matrix and background
void print2d(char** a, int p, int q, int mode, int indexBackground) {
	setColor(rand() % 10 + 1);
	backgroundPlay(indexBackground);
	for (int i = 0; i < p; i++)
		for (int j = 0; j < q; j++)
		{
			if (a[i][j] == ' ')
				continue;
			else
			{
				box(2 + j * 8, 2 + i * 4, 4, 8, a[i][j], mode, 8);
			}
		}
}


bool IMatch(char** a, int posRow1, int posCol1, int posRow2, int posCol2) {
	if (posRow1 == posRow2) {
		int x, y;
		if (posCol2 > posCol1) {
			x = posCol1;
			y = posCol2;
		}
		else {
			x = posCol2;
			y = posCol1;
		}
		for (int i = x + 1; i < y; i++) {
			if (a[posRow1][i] != 32) {
				return false;
			}
		}
		return true;
	}

	if (posCol1 == posCol2) {
		int x, y;
		if (posRow2 > posRow1) {
			x = posRow1;
			y = posRow2;
		}
		else {
			x = posRow2;
			y = posRow1;
		}
		for (int i = x + 1; i < y; i++) {
			if (a[i][posCol2] != 32) {
				return false;
			}
		}
		return true;
	}
	return false;
}

bool lineCheck(char** a, int posRow1, int posCol1, int posRow2, int posCol2) { // Using for ZMatch
	if (posRow1 == posRow2) {
		int x, y;
		if (posCol2 > posCol1) {
			x = posCol1;
			y = posCol2;
		}
		else {
			x = posCol2;
			y = posCol1;
		}
		for (int i = x; i <= y; i++) {
			if (a[posRow1][i] != 32) {
				return false;
			}
		}
		return true;
	}

	if (posCol1 == posCol2) {
		int x, y;
		if (posRow2 > posRow1) {
			x = posRow1;
			y = posRow2;
		}
		else {
			x = posRow2;
			y = posRow1;
		}
		for (int i = x; i <= y; i++) {
			if (a[i][posCol2] != 32) {
				return false;
			}
		}
		return true;
	}
	return false;
}

bool ZMatch(char** a, int posRow1, int posCol1, int posRow2, int posCol2) {
	if (posRow1 == posRow2 || posCol1 == posCol2)
		return false;
	int x, y;
	if (posCol1 < posCol2)
	{
		x = posCol1;
		y = posCol2;
		for (int i = x + 1; i < y; i++)
		{
			if (lineCheck(a, posRow1, i, posRow2, i))
			{
				if (lineCheck(a, posRow1, posCol1 + 1, posRow1, i) && lineCheck(a, posRow2, posCol2 - 1, posRow2, i))
					return true;
			}
		}
	}
	else
	{
		x = posCol2;
		y = posCol1;
		for (int i = x + 1; i < y; i++)
		{
			if (lineCheck(a, posRow1, i, posRow2, i))
			{
				if (lineCheck(a, posRow1, posCol1 - 1, posRow1, i) && lineCheck(a, posRow2, posCol2 + 1, posRow2, i))
					return true;
			}
		}
	}


	if (posRow1 < posRow2)
	{
		x = posRow1;
		y = posRow2;
		for (int i = x + 1; i < y; i++)
		{
			if (lineCheck(a, i, posCol1, i, posCol2))
			{
				if (lineCheck(a, posRow1 + 1, posCol1, i, posCol1) && lineCheck(a, posRow2 - 1, posCol2, i, posCol2))
					return true;
			}
		}
	}
	else
	{
		x = posRow2;
		y = posRow1;
		for (int i = x + 1; i < y; i++)
		{
			if (lineCheck(a, i, posCol1, i, posCol2))
			{
				if (lineCheck(a, posRow1 - 1, posCol1, i, posCol1) && lineCheck(a, posRow2 + 1, posCol2, i, posCol2))
					return true;
			}
		}
	}

	return false;
}

bool LMatch(char** a, int posRow1, int posCol1, int posRow2, int posCol2)
{
	if (posRow1 == posRow2 || posCol1 == posCol2)
		return false;
	bool check1, check2; // kiem tra 2 duong thang ghep lai thanh L
	if (a[posRow1][posCol2] == ' ') {
		check1 = IMatch(a, posRow1, posCol1, posRow1, posCol2);
		check2 = IMatch(a, posRow2, posCol2, posRow1, posCol2);
		if (check1 && check2) {
			return true;
		}
	}

	if (a[posRow2][posCol1] == ' ') {
		check1 = IMatch(a, posRow1, posCol1, posRow2, posCol1);
		check2 = IMatch(a, posRow2, posCol2, posRow2, posCol1);
		if (check1 && check2) {
			return true;
		}
	}
	return false;
}

bool UMatch(char** a, int p, int q, int posRow1, int posCol1, int posRow2, int posCol2) {
	if ((posRow1 == 0 && posRow2 == 0) || (posRow1 == p - 1 && posRow2 == p - 1))
		return true;
	if ((posCol1 == 0 && posCol2 == 0) || (posCol1 == q - 1 && posCol2 == q - 1))
		return true;

	// Upper U check
	int up;
	if (posRow1 < posRow2)
		up = posRow1;
	else
		up = posRow2;

	if (IMatch(a, posRow1, posCol1, -1, posCol1) && IMatch(a, posRow2, posCol2, -1, posCol2))
		return true;
	else
		for (int i = up - 1; i >= 0; i--) {
			if (IMatch(a, posRow1, posCol1, i - 1, posCol1) && IMatch(a, posRow2, posCol2, i - 1, posCol2))
				if (IMatch(a, i, posCol1, i, posCol2))
					return true;
		}


	//Right U check
	int right;
	if (posCol1 < posCol2)
		right = posCol2;
	else
		right = posCol1;

	if (IMatch(a, posRow1, posCol1, posRow1, q) && IMatch(a, posRow2, posCol2, posRow2, q))
		return true;
	else
		for (int i = right + 1; i < q; i++) {
			if (IMatch(a, posRow1, posCol1, posRow1, i + 1) && IMatch(a, posRow2, posCol2, posRow2, i + 1))
				if (IMatch(a, posRow1, i, posRow2, i))
					return true;
		}



	//Left U check
	int left;
	if (posCol1 < posCol2)
		left = posCol1;
	else
		left = posCol2;

	if (IMatch(a, posRow1, posCol1, posRow1, -1) && IMatch(a, posRow2, posCol2, posRow2, -1))
		return true;
	else
		for (int i = left - 1; i >= 0; i--) {
			if (IMatch(a, posRow1, posCol1, posRow1, i - 1) && IMatch(a, posRow2, posCol2, posRow2, i - 1))
				if (IMatch(a, posRow1, i, posRow2, i))
					return true;
		}



	//Down U check
	int down;
	if (posRow1 < posRow2)
		down = posRow2;
	else
		down = posRow1;

	if (IMatch(a, posRow1, posCol1, p, posCol1) && IMatch(a, posRow2, posCol2, p, posCol2))
		return true;
	else
		for (int i = down + 1; i < p; i++) {
			if (IMatch(a, posRow1, posCol1, i + 1, posCol1) && IMatch(a, posRow2, posCol2, i + 1, posCol2))
				if (IMatch(a, i, posCol1, i, posCol2))
					return true;
		}

	// When there's not any way to match
	return false;
}


// check whether two chosen cells are correct
bool checkAll(char** a, int p, int q, int posRow1, int posCol1, int posRow2, int posCol2) {

	// if two cells have the same position, the match is false
	if (a[posRow1][posCol1] != a[posRow2][posCol2] || (posRow1 == posRow2 && posCol1 == posCol2))
		return false;
	if (a[posRow1][posCol1] == ' ' || a[posRow2][posCol2] == ' ')
		return false;
	if (a[posRow1][posCol1] == a[posRow2][posCol2])
	{
		if (IMatch(a, posRow1, posCol1, posRow2, posCol2)) { // check I match
			return true;
		}
		if (LMatch(a, posRow1, posCol1, posRow2, posCol2)) { // check L match
			return true;
		}
		if (ZMatch(a, posRow1, posCol1, posRow2, posCol2)) { // check Z match
			return true;
		}
		if (UMatch(a, p, q, posRow1, posCol1, posRow2, posCol2)) { // check U match
			return true;
		}
	}
	return false;;
}

// check the number of pairs in matrix
bool checkExistPair(char** a, int p, int q) {
	for (int i = 0; i < p; i++) {
		for (int j = 0; j < q; j++) {
			for (int k = i; k < p; k++) {
				for (int l = j; l < q; l++) {
					if (a[i][j] == ' ' || a[k][l] == ' ' || ((k == i) && (l == j) )) {
						continue;
					}
					else if (checkAll(a, p, q, i, j, k, l))
						return true;
				}
			}
		}
	}
	return false;
}

// if the match is successful, remove 2 chosen cells by replacing the values in them as a space character
void resetEle(char** a, int p, int q, int posRow1, int posCol1, int posRow2, int posCol2, int choice) {
	if (checkAll(a, p, q, posRow1, posCol1, posRow2, posCol2)) {
			a[posRow1][posCol1] = ' ';
			a[posRow2][posCol2] = ' ';
	}
}


// change x y coordinates when pressing UP from the keyboard
void moveUp(char** a, int p, int q, int& x, int& y) {
	for (int i = x - 1; i >= 0; i--)
		if (a[i][y] != ' ')
		{
			x = i;
			return;
		}

	for (int i = x - 1; i >= 0; i--)
		for (int j = 1; j < q; j++)
		{
			if (y - j >= 0 && a[i][y - j] != ' ')
			{
				x = i;
				y = y - j;
				return;
			}
			if (y + j < q && a[i][y + j] != ' ')
			{
				x = i;
				y = y + j;
				return;
			}
		}
}

// change x y coordinates when pressing DOWN from the keyboard
void moveDown(char** a, int p, int q, int& x, int& y) {
	for (int i = x + 1; i < p; i++)
		if (a[i][y] != ' ')
		{
			x = i;
			return;
		}

	for (int i = x + 1; i < p; i++)
		for (int j = 1; j < q; j++)
		{
			if (y - j >= 0 && a[i][y - j] != ' ')
			{
				x = i;
				y = y - j;
				return;
			}
			if (y + j < q && a[i][y + j] != ' ')
			{
				x = i;
				y = y + j;
				return;
			}
		}
}

// change x y coordinates when pressing LEFT from the keyboard
void moveLeft(char** a, int p, int q, int& x, int& y) {
	for (int j = y - 1; j >= 0; j--)
		if (a[x][j] != ' ')
		{
			y = j;
			return;
		}

	for (int j = y - 1; j >= 0; j--)
		for (int i = 1; i < p; i++)
		{
			if (x - i >= 0 && a[x - i][j] != ' ')
			{
				x = x - i;
				y = j;
				return;
			}
			if (x + i < p && a[x + i][j] != ' ')
			{
				x = x + i;
				y = j;
				return;
			}
		}
}

// change x y coordinates when pressing RÌGHT from the keyboard
void moveRight(char** a, int p, int q, int& x, int& y) {
	for (int j = y + 1; j < q; j++)
		if (a[x][j] != ' ')
		{
			y = j;
			return;
		}
	
	for (int j = y + 1; j < q; j++)
		for (int i = 1; i < p; i++)
		{
			if (x - i >= 0 && a[x - i][j] != ' ')
			{
				x = x - i;
				y = j;
				return;
			}
			if (x + i < p && a[x + i][j] != ' ')
			{
				x = x + i;
				y = j;
				return;
			}
		}
}

// create random x y coordinates of the pointer after matching successfully
void randomPos(char** a, int p, int q, int& x, int& y) {
	srand(time(NULL));
	while (a[x][y] == ' ')
	{
		x = rand() % p;
		y = rand() % q;
	}
}
