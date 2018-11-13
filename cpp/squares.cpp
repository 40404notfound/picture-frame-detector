// The "Square Detector" program.
// It loads several images sequentially and tries to find squares in
// each image

#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include <iostream>
#include <math.h>
#include <string.h>
#include <filesystem>
#include <vector>
#include <string>

using namespace std::filesystem;

using namespace cv;
using namespace std;




const char* wndname = "Square Detection Demo";

// helper function:
// finds a cosine of angle between vectors
// from pt0->pt1 and from pt0->pt2
static double angle( Point pt1, Point pt2, Point pt0 )
{
    double dx1 = pt1.x - pt0.x;
    double dy1 = pt1.y - pt0.y;
    double dx2 = pt2.x - pt0.x;
    double dy2 = pt2.y - pt0.y;
    return (dx1*dx2 + dy1*dy2)/sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 1e-10);
}

struct para
{
	int canny1;
	int canny2;
	int canny3;
	int N;
	double appro;

};
para p{ 5,50,1,10,0.02 };
static void findSquares(const Mat& image, vector<vector<Point> >& squares,para& p)
{
	

	Mat timg;
	image.copyTo(timg);


	medianBlur(image, timg, 9);
	Mat gray0(timg.size(), CV_8U), gray;

	vector<vector<Point> > contours;


	for (int c = 0; c < 3; c++)
	{
		int ch[] = { c, 0 };
		mixChannels(&timg, 1, &gray0, 1, ch, 1);


		//cv::Scalar avg, sdv;
		//cv::meanStdDev(gray0, avg, sdv);
		//sdv.val[0] = sqrt(gray0.cols*gray0.rows*sdv.val[0] * sdv.val[0]);
		//cout << sdv.val[0] << endl;
		//sdv.val[0] = 1;
		//gray0.convertTo(gray0, CV_8U, 1 / sdv.val[0], -avg.val[0] / sdv.val[0]);
		

		// try several threshold levels
		for (int l = 0; l < p.N; l++)
		{

			if (l == 0)
			{

				Canny(gray0, gray, p.canny1, p.canny2, p.canny3*2+1);

				dilate(gray, gray, Mat(), Point(-1, -1));
				
			}
			else
			{

				gray = gray0 >= (l + 1) * 255 / p.N;
			}

			findContours(gray, contours, RETR_LIST, CHAIN_APPROX_SIMPLE);

			vector<Point> approx;

			for (size_t i = 0; i < contours.size(); i++)
			{

				approxPolyDP(Mat(contours[i]), approx, arcLength(Mat(contours[i]), true)*p.appro, true);


				if (approx.size() == 4 &&
					fabs(contourArea(Mat(approx))) > 1000 &&
					isContourConvex(Mat(approx)))
				{
					double maxCosine = 0;

					for (int j = 2; j < 5; j++)
					{

						double cosine = fabs(angle(approx[j % 4], approx[j - 2], approx[j - 1]));
						maxCosine = MAX(maxCosine, cosine);
					}


					if (maxCosine < 0.3)
						squares.push_back(approx);
				}
			}
		}
	}
}



static void drawSquares( Mat& image, const vector<vector<Point> >& squares,string title )
{
	Mat timg;
	image.copyTo(timg);
	

    for( size_t i = 0; i < squares.size(); i++ )
    {
        const Point* p = &squares[i][0];

        int n = (int)squares[i].size();

        if (p-> x > 3 && p->y > 3)
          polylines(timg, &p, &n, 1, true, Scalar(0,255,0), 3, LINE_AA);
    }

    imshow(title, timg);
}
Mat image;
string name;
vector<vector<Point> > squares;
vector<string> names;
int previous=-1;
int cursor=0;
void onChangeTrackBar(int poi, void* usrdata)
{
	if (previous != cursor)
	{
		previous = cursor;
		string name = names[cursor];
		image = imread(name, 1);
		resize(image, image, { 600,800 }, 0, 0, INTER_CUBIC);
	}

	squares.clear();
	findSquares(image, squares, p);

	drawSquares(image, squares, "demo");
}

int main(int /*argc*/, char** /*argv*/)
{
	
	
	for (auto & p : directory_iterator("photos"))
		names.push_back(p.path().string());
	namedWindow("demo", WINDOW_NORMAL);
    
		

		
	createTrackbar("canny1", "demo", &p.canny1, 200,onChangeTrackBar, 0);
	createTrackbar("canny2", "demo", &p.canny2, 200, onChangeTrackBar, 0);
	createTrackbar("canny3", "demo", &p.canny3, 10, onChangeTrackBar, 0);
	createTrackbar("N", "demo", &p.N, 20, onChangeTrackBar, 0);
	createTrackbar("image", "demo", &cursor, names.size()-1, onChangeTrackBar, 0);
		
	while (waitKey() != 'e');

    return 0;
}
