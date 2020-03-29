#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>     /* rand */
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
	string result;
	string startstring = "00000";
	while (true) {
		string input = generate_random_string(247);
		string output = sha256(input);
		if (startstring.compare(output.substr(0,5)) == 0) {
			// cout << "sha256('"<< input << "'):" << output << endl;
			std::ofstream outfile;
			outfile.open("result.txt", std::ios_base::app); // append instead of overwrite
			outfile << input << endl;
		}
	}
}
