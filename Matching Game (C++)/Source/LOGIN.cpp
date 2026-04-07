#include "LOGIN.h"
#include "GRAPHICS.h"
#include "MENU.h"
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

// external menu when logged in
void start() {
	resizeConsole(1000, 600);
	setColor(15);
	ShowCur(0);
	system("cls");
	gotoxy(10, 1);

	// draw background
	cout << "\t\t\t______________________________________________________\n\n";
	ifstream ifs("pikachu.txt");
	int i = 0;
	while (!ifs.eof())
	{
		gotoxy(10, 1 + i + 1);
		setColor(11);
		string s;
		getline(ifs, s);
		cout << "\t\t" << s << endl;
		i++;
	}
	gotoxy(10, 1 + i + 2);
	ifs.close();
	setColor(15);
	cout << "\t\t\t_____________           MENU         _____________\n\n";
	cout << "                                                           \n\n";
	i = i + 2;
	string s[5] = { "       Login" , "      Register", "  Forgot password", "       Help", "        Exit" };

	// draw options
	box2(48, 1 + i + 2, 20, 2, 15, s[0]);
	box2(48, 1 + i + 2 + 4, 20, 2, 15, s[1]);
	box2(48, 1 + i + 2 + 8, 20, 2, 15, s[2]);
	box2(48, 1 + i + 2 + 12, 20, 2, 15, s[3]);
	box2(48, 1 + i + 2 + 16, 20, 2, 15, s[4]);

	int c;
	box2(48, 1 + i + 2, 20, 2, 9, s[0]);
	int countString = 0;
	int oldString = 0;
	while (true) {
		box2(48, 1 + i + 2 + oldString * 4, 20, 2, 15, s[oldString]);
		box2(48, 1 + i + 2 + countString * 4, 20, 2, 9, s[countString]);
		oldString = countString;

		switch (c = _getch())
		{
			case UP:
				countString -= 1;
				if (countString == -1)
					countString = 4;
				break;
			case DOWN:
				countString += 1;
				if (countString == 5)
					countString = 0;
				break;
			case ENTER:
			{
				setColor(15);
				if (countString == 0)
					login();
				else if (countString == 1)
					registration();
				else if (countString == 2)
					forgot();
				else if (countString == 3)
					help();
				else
				{
					system("cls"); exit(1); break;
				}
			}
		}
		
	}

}


void login() {
	system("cls");
	ShowCur(1);

	bool checkName = false;
	bool checkPass = false;
	string userName, password, name, pass;

	cout << "Enter your username: "; cin >> userName;
	cout << "Enter your password: "; cin >> password;

	//check existence of username and password in file.
	ifstream input("records.txt");
	int posPlayer = 0;
	while (!input.eof()) {
		checkName = false;
		checkPass = false;

		input >> name >> pass;

		if (userName == name)
			checkName = true;

		if (pass == password)
			checkPass = true;

		if (checkPass && checkName)
		{
			system("cls");
			cout << "Your LOGIN is successful\nThanks for Logging in !\nLoading...";
			this_thread::sleep_for(chrono::seconds(1));
			break;
		}

		string garbage; // ignore score of player
		getline(input, garbage);

		posPlayer++;

	}
	input.close();

	if (!checkPass || !checkName) {
		cout << "\nLOGIN ERROR \nPlease check your username and password\n";
		this_thread::sleep_for(chrono::seconds(1));
		start();
	}
	else {
		system("cls");
		menu(posPlayer);
	}

}

void registration() {
	system("cls");
	ShowCur(1);

	string ruserName, rpassword, rpass, rname;
	
	ifstream ifs("records.txt");
	cout << "\t\t\t Enter the username: "; cin >> ruserName;
	cout << "\t\t\t Enter the password: "; cin >> rpassword;

	while (!checkRegistration("records.txt", ruserName, rpassword))
	{
		system("cls");
		cout << "\t\t\t Your username is existed, please enter again!\n\n";
		cout << "\t\t\t Enter the username: "; cin >> ruserName;
		cout << "\t\t\t Enter the password: "; cin >> rpassword;
	}
	ifs.close();


	ofstream save("records.txt", ios::app);
	save << ruserName << " " << rpassword << " " << 0 << " " << 0 << " " << 0 << endl;
	system("cls");
	setColor(15);
	cout << "\n\t\t\t Registration is successfull! \n";
	this_thread::sleep_for(chrono::seconds(2));
	save.close();
	start();

}

bool checkRegistration(string file, string username, string password) {
	string name, pass;
	ifstream ifs(file);
	while (!ifs.eof())
	{
		ifs >> name >> pass;
		if (name == username)
			return false;
	}
	ifs.close();
	return true;
}

void forgot() {
	system("cls");
	ShowCur(1);

	int option;

	cout << "\t\t You forgot the password? No worries \n\n";
	cout << "\t\t Press 1  || search your id by username" << endl;
	cout << "\t\t Press 2  || go back the main menu \n\n";
	cout << "\t\t Enter your choice : ";
	cin >> option;
	switch (option) {
	case 1:
	{
		string suserName, sname, spass;
		cout << "\n\t\t Enter the username which you remembered: ";
		cin >> suserName;

		ifstream f1("records.txt");
		bool check = false;
		while (!f1.eof())
		{
			f1 >> sname;
			f1 >> spass;
			if (sname == suserName)
			{
				system("cls");
				check = true;
				cout << "\n\t\t Your username is found! \n";
				cout << "\t\t===>";
				cout << " Your password is: " << spass << endl << endl;
				this_thread::sleep_for(chrono::seconds(2));
				start();
				break;
			}
			string garbage;
			getline(f1, garbage);
		}
		f1.close();
		if (check == false) {
			cout << "\n\t\t-------------------------------------";
			cout << "\n\t\t Sorry! your account is not found! \n\n";
			this_thread::sleep_for(chrono::seconds(2));
			start();
		}
		break;
	}

	case 2:
		start();
	default:
		cout << "\t\t\t Wrong choice! Please try again " << endl;
		forgot();
	}
}

void help() {
	ShowCur(0);
	resizeConsole(1000, 600);
	system("cls");
	ifstream read("help.txt");
	int i = 1;
	while (!read.eof())
	{
		setColor(14);
		if (i <= 8)
			setColor(11);
		string s;
		getline(read, s, '\n');
		gotoxy(20, 8 + i);
		cout << s << endl;
		i++;
	}
	read.close();

	gotoxy(45, 10  + 1 + i);
	setColor(4);
	cout << "Press ESC to back to Login Menu";
	int c;
	do {
		c = _getch();
	} while (c != ESC);
	start();
}