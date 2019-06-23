#include <memory>

typedef unsigned char uchar;
typedef unsigned int QRgb;

inline QRgb qRgb(int r, int g, int b) {
    return (0xffu << 24) | ((r & 0xffu) << 16) | ((g & 0xffu) << 8) | (b & 0xffu); }
// 0..255 gray value
inline int qGray(QRgb rgb) {
    return (((rgb >> 16) & 0xff)*11+((rgb >> 8) & 0xff)*16+(rgb & 0xff)*5)/32;}

extern "C"
{
    void adaptiveIntegralThresh(uchar *data, int w, int h, int bpl);
}


#define Row(y) ((QRgb*)(data+(y)*bpl))

void adaptiveIntegralThresh(uchar *data, int w, int h, int bpl)
{
    // Allocate memory for integral image
    int *ptr, **intImg;
    int len = sizeof(int *) * h + sizeof(int) * w * h;
    intImg = (int **)malloc(len);

    ptr = (int*)(intImg + h);
    for(int i = 0; i < h; i++)
        intImg[i] = (ptr + w * i);

    // Calculate integral image
    for (int y=0;y<h;++y)
    {
        QRgb *row = Row(y);
        int sum=0;
        for (int x=0;x<w;++x)
        {
            sum += qGray(row[x]);
            if (y==0)
                intImg[y][x] = qGray(row[x]);
            else
                intImg[y][x] = intImg[y-1][x] + sum;
        }
    }
    // Apply Adaptive threshold (tune value of k and s to get expected result)
    float k = 0.15; // higher value, narrower text
    int s = w/32;   // lower value, more white
    int s2 = s/2;
    int x1,y1,x2,y2, count, sum, md;
    for (int i=0;i<h;++i)
    {
        y1 = ((i - s2)>0) ? (i - s2) : 0;
        y2 = ((i + s2)<h) ? (i + s2) : h-1;
        QRgb *row = Row(i);
        for (int j=0;j<w;++j)
        {
            x1 = ((j - s2)>0) ? (j - s2) : 0;
            x2 = ((j + s2)<w) ? (j + s2) : w-1;

            count = (x2 - x1)*(y2 - y1);
            sum = intImg[y2][x2] - intImg[y2][x1] - intImg[y1][x2] + intImg[y1][x1];
            md = qGray(row[j]) - sum/count;     // mean deviation

            if ( qGray(row[j]) < sum/count *(1+ k*(md/128-1)) )
                row[j] = qRgb(0,0,0);
            else
                row[j] = qRgb(255,255,255);
        }
    }
    free(intImg);
}
