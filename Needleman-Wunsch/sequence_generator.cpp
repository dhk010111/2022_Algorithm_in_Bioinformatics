// ���߼��������� �õ��� sequence�� �����ϴ� �ڵ� (4���� �ǽ� �ڵ带 ���� �����Ͽ� ����)
//���� 20�� ������ ���⼭���� 10�ۼ�Ʈ�� ���̸� ���̴� ���⼭�� 20�� �Ǵ� 7���� �����Ͽ� sequence.txt�� �����Ѵ�.

#include <iostream>
#include<fstream>
#include <ctime>
#include <random>
#include <string>
#include<algorithm>

using namespace std;

//���� N�� ������ ���⼭���� �����Ͽ� origin.txt�� �����ϴ� �Լ�

void makeOriginDNA(int n)
{
    //���� ���� �غ�
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dis(0, 3);

    //���� �Է� �غ�
    ofstream ofs;
    ofs.open("origin.txt");


    //0, 1, 2, 3 �� ������ �����ϰ� ������ ��쿡 A, C, G, T�� origin.txt�� �Է��Ѵ�.
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

//origin�� 10�ۼ�Ʈ�� ���̸� ���̴� mutation.txt�� �����ϴ� �Լ�
void makemutation(int n, int num)
{
    //���� ���� �غ�
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dis(0, n - 1);


    for (size_t x = 0; x < num; x++)
    {

        //���� ��ġ�� n/10�� �����Ͽ� SNPpose �迭�� �����Ѵ�. (�������� ����)
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