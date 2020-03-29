#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>     /* srand, rand */
#include <sys/types.h>
#include <unistd.h>
#include "sha256.h"


using namespace std;
using std::string;
using std::cout;
using std::endl;


string generate_random_string(int len)
{
	int pos;
	string str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
	string newstr = "h25";
	while(newstr.size() != 3 + len) {
		pos = ((rand() % (str.size())));
		newstr += str.substr(pos, 1);
	}
	return newstr;
}


int main(int argc, char *argv[])
{
	int input_len;
	string result;
	string startstring = "00000";
	srand(getpid());
	while (true) {
		input_len = 232 + ((rand() % 145));
		string input = generate_random_string(input_len);
		string output = sha256(input);
		if (startstring.compare(output.substr(0,5)) == 0) {
			cout << "sha256('"<< input << "'):" << output << endl;
			std::ofstream outfile;
			outfile.open("result.txt", std::ios_base::app); // append instead of overwrite
			outfile << input << endl;
		}
	}
}
