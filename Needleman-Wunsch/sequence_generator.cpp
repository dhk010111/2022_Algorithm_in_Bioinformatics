// 다중서열정렬을 시도할 sequence를 생성하는 코드 (4주차 실습 코드를 조금 변형하여 재사용)
//길이 20의 무작위 염기서열과 10퍼센트의 차이를 보이는 염기서열 20개 또는 7개를 생성하여 sequence.txt에 저장한다.

#include <iostream>
#include<fstream>
#include <ctime>
#include <random>
#include <string>
#include<algorithm>

using namespace std;

//길이 N의 무작위 염기서열을 생성하여 origin.txt로 저장하는 함수

void makeOriginDNA(int n)
{
    //난수 생성 준비
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dis(0, 3);

    //파일 입력 준비
    ofstream ofs;
    ofs.open("origin.txt");


    //0, 1, 2, 3 의 난수를 생성하고 각각의 경우에 A, C, G, T를 origin.txt에 입력한다.
    for (int i = 0; i < n; i++)
    {
        int seq = dis(gen);

        string s;
        if (seq == 0)
            s = "A";
        else if (seq == 1)
            s = "C";
        else if (seq == 2)
            s = "G";
        else if (seq == 3)
            s = "T";
        ofs.write(s.c_str(), 1);
    }


}

//origin과 10퍼센트의 차이를 보이는 mutation.txt를 생성하는 함수
void makemutation(int n, int num)
{
    //난수 생성 준비
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dis(0, n - 1);


    for (size_t x = 0; x < num; x++)
    {

        //변이 위치를 n/10개 선정하여 SNPpose 배열에 저장한다. (오름차순 정렬)
        int* SNPpos = new int[n / 10];

        for (int i = 0; i < n / 10; i++)
        {
            SNPpos[i] = dis(gen);
            for (int j = 0; j < i; j++)
            {
                if (SNPpos[i] == SNPpos[j])
                {
                    i--;
                }
            }
        }
        sort(SNPpos, SNPpos + n / 10);

        ifstream ifs("origin.txt");
        ofstream fout("mutation.txt", ios_base::app);
        int nextSNPindex = 0;
        for (int i = 0; i < n; i++)
        {
            if (i == SNPpos[nextSNPindex])
            {
                char seq;
                ifs >> seq;
                if (seq == 'A')
                    fout << 'T';
                else if (seq == 'T')
                    fout << 'G';
                else if (seq == 'G')
                    fout << 'C';
                else if (seq == 'C')
                    fout << 'A';
                nextSNPindex++;
            }
            else
            {
                char seq;
                ifs >> seq;
                fout << seq;
            }


        }
        fout << ',';
    }


}

int main()
{
    int N = 20;
    int num = 20;

    makeOriginDNA(N);
    cout << "1" << endl;
    makemutation(N,num);
    cout << "2" << endl;
}