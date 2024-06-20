#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int *stringToArray_reverse(const char *str, int *size)
{
    *size = strlen(str);
    int *arr = (int *)malloc(sizeof(int) * (*size));
    int j = 0;

    for (int i = *size - 1; i >= 0; i--)
    {
        arr[j] = str[i] - '0';
        if (arr[j] > 9 || arr[j] < 0)
        {
            printf("The input cannot be interpret as numbers!");
            break;
        }
        j++;
    }

    return arr;
}

void Integer_add(int op1[], int op2[], int len1, int len2)
{
    int carry = 0;
    int maxSize = len1 > len2 ? len1 : len2;
    // 这里多留了一位，用来处理有可能最后有进位
    int res[1001] = {0};
    int k = 0;

    int i = 0, j = 0;
    // 这里表示进位的操作，将余数存进答案数组，进位存进carry直到数组原数组遍历完
    while (i <= len1 - 1 || j <= len2 - 1)
    {
        int sum = carry;
        if (i <= len1 - 1)
            sum += op1[i++];
        if (j <= len2 - 1)
            sum += op2[j++];
        res[k++] = sum % 10;
        carry = sum / 10;
    }

    res[maxSize] = carry;
    if (carry > 0)
    {
        for (int i = maxSize; i >= 0; i--)
            printf("%d", res[i]);
    }
    else
    {
        for (int i = maxSize - 1; i >= 0; i--)
            printf("%d", res[i]);
    }
}

void Integer_subtract(char op1[], char op2[], int len1, int len2)
{
    int is_neg = 0;
    int len = 0;
    int a[1001] = {0}, b[1001] = {0};
    // 判断哪个字符串比较大
    if (len1 < len2 || (strcmp(op1, op2) < 0 && len1 == len2))
    {
        // 这里将字符串判断之后再进行倒序输入
        is_neg = 1;
        for (int i = len2 - 1; i >= 0; i--)
            a[len2 - i - 1] = op2[i] - '0';
        for (int i = len1 - 1; i >= 0; i--)
            b[len1 - i - 1] = op1[i] - '0';
    }
    else
    {
        for (int i = len1 - 1; i >= 0; i--)
            a[len1 - i - 1] = op1[i] - '0';
        for (int i = len2 - 1; i >= 0; i--)
            b[len2 - i - 1] = op2[i] - '0';
    }
    // 将长度赋值为长度较长的数
    if (len1 > len2)
        len = len1;
    else
        len = len2;
    // 核心计算，如果需要借位的话a[i+1]--
    for (int i = 0; i < len; i++)
    {
        a[i] = a[i] - b[i];
        if (a[i] < 0)
        {
            a[i + 1] -= 1;
            a[i] += 10;
        }
    }
    while (a[len - 1] == 0 && len > 1)
        len--;
    if (is_neg == 1)
        printf("-");
    for (int i = len - 1; i >= 0; i--)
        printf("%d", a[i]);
}

void Integer_multiply(int op1[], int op2[], int len1, int len2, int decimal)
{
    // 这里函数变量中decimal表示小数点需要移动的位数，主要是为后续的Decimal_multiply计算服务
    // maxSize表示最长的可能长度
    int maxSize = len1 + len2;
    int i, j;

    int result[maxSize];
    // 将结果数组初始化为0
    for (i = 0; i < maxSize; i++)
    {
        result[i] = 0;
    }
    // 核心计算过程，逐位相乘并累加
    for (i = 0; i < len1; i++)
    {
        for (j = 0; j < len2; j++)
        {
            result[i + j] += op1[i] * op2[j];
            result[i + j + 1] += result[i + j] / 10;
            result[i + j] %= 10;
        }
    }
    // 标记开始点
    int start = 0;
    for (int i = maxSize - 1; i >= 0; i--)
    {
        if (result[i] != 0)
        {
            start = i;
            break;
        }
    }
    for (int i = start; i >= decimal; i--)
    {
        printf("%d", result[i]);
    }
    if (decimal != 0)
        printf(".");
    for (int i = decimal - 1; i >= 0; i--)
    {
        printf("%d", result[i]);
    }
}
// 此函数判断除法操作中被除数是不是继续做减法
int judge_if_continuediv(int a[], int b[], int len)
{
    // 发现a较小就直接退出
    int res = 1;
    for (int i = len - 1; i >= 0; i--)
    {
        if (a[i] < b[i])
        {
            res = 0;
            break;
        }
        else if (a[i] > b[i])
            break;
    }
    return res;
}
// 此函数计算除法操作最后的低精度除法
float ints_to_float(int num[], int len)
{
    float result = 0.0;
    int i;
    // 对数组中的每个数字进行转换并相加
    for (i = len - 1; i >= 0; i--)
    {
        result = result * 10 + num[i];
    }

    return result;
}

void Integer_division(char op1[], char op2[], int len1, int len2, int decimal)
{
    // 这里模拟的高精度/低精度除法，即除数只能是低精度的参数(int 类型可以存储的)
    if (len1 < len2 || len1 == len2 && strcmp(op1, op2) < 0)
    {
        double double_num1 = atof(op1);
        double double_num2 = atof(op2);
        long double double_ans = double_num1 / double_num2;
        char ans0[1001] = {0};
        sprintf(ans0, "%Lf", double_ans);
        int length = strlen(ans0);
        if (decimal <= 0)
        {
            printf("0.");
            for (int i = 0; i < abs(decimal); i++)
                printf("0");
            for (int i = 2; i < length; i++)
                printf("%c", ans0[i]);
        }
        else
        {
            int start = 2;
            for (int i = 2; i < length; i++)
            {
                if (ans0[i] != '0')
                {
                    start = i;
                    break;
                }
            }
            for (int i = start; i < abs(decimal) + 2; i++)
                printf("%c", ans0[i]);
            printf(".");
            for (int i = abs(decimal) + 2; i < length; i++)
                printf("%c", ans0[i]);
        }
    }

    else
    {
        int len = len1;
        int a[1001] = {0}, b[1001] = {0};
        // 判断哪个字符串比较大
        for (int i = len1 - 1; i >= 0; i--)
            a[len1 - i - 1] = op1[i] - '0';
        for (int i = len2 - 1; i >= 0; i--)
            b[len2 - i - 1] = op2[i] - '0';
        int quo = 0;
        while (len > len2 || (len == len2 && judge_if_continuediv(a, b, len) == 1))
        {
            for (int i = 0; i < len; i++)
            {
                a[i] = a[i] - b[i];
                if (a[i] < 0)
                {
                    a[i + 1] -= 1;
                    a[i] += 10;
                }
            }
            while (a[len - 1] == 0 && len > 1)
                len--;
            quo++;
        }
        char quo_str[1001] = {0};
        // 减完之后直接输出整数部分，小数部分后续直接计算
        sprintf(quo_str, "%d", quo);
        int leng = strlen(quo_str);
        if (decimal < 0)
        {
            if (decimal + leng <= 0)
            {
                printf("0.");
                for (int i = 0; i < (abs(decimal) - leng); i++)
                    printf("0");
                printf("%d", quo);
            }
            else
            {
                for (int i = 0; i < (decimal + leng); i++)
                    printf("%c", quo_str[i]);
                printf(".");
                for (int i = decimal + leng; i < leng; i++)
                    printf("%c", quo_str[i]);
            }
            if (len != 0)
            {
                float r1 = ints_to_float(a, len);
                float r2 = ints_to_float(b, len2);
                float ans = r1 / r2;
                char str[1001] = {0};
                // 这里将15位的浮点数转化并存储为str
                sprintf(str, "%.15f", ans);
                for (int i = 2; i < 10; i++)
                    printf("%c", str[i]);
            }
        }
        else
        {
            printf("%d", quo);
            if (len != 0)
            {
                float r1 = ints_to_float(a, len);
                float r2 = ints_to_float(b, len2);
                float ans = r1 / r2;
                char str[1001] = {0};
                sprintf(str, "%.15f", ans);
                for (int i = 2; i < 2 + decimal; i++)
                    printf("%c", str[i]);
                printf(".");
                for (int i = 2 + decimal; i < 10; i++)
                    printf("%c", str[i]);
            }
        }
    }
}
// 此函数在小数计算的时候直接判断小数点的位置
int find_decimalpoint(char op[], int len)
{
    int find_dec = len - 1;
    for (int i = 0; i < len; i++)
    {
        if (op[i] == '.')
        {
            find_dec = i;
            break;
        }
    }
    return find_dec;
}
// 此函数在于判断字符串中科学计数法的位置
int find_sci(char op[], int len)
{
    int find_sci = len - 1;
    for (int i = 0; i < len; i++)
    {
        if (op[i] == 'e')
        {
            find_sci = i;
            break;
        }
    }
    return find_sci;
}

void Decimal_add(char op1[], char op2[], int len1, int len2)
{
    // 找到数中小数点以及科学计数法的位置
    int find_dec1 = find_decimalpoint(op1, len1);
    int find_dec2 = find_decimalpoint(op2, len2);

    int find_sci1 = find_sci(op1, len1);
    int find_sci2 = find_sci(op2, len2);

    char dec1part[1001] = {0}, dec2part[1001] = {0};
    char int1part[1001] = {0}, int2part[1001] = {0};
    // 这里把两个数的整数和小数部分全部分开，并且利用函数添加到不同的String中
    strncpy(dec1part, op1 + find_dec1 + 1, len1 - find_dec1 - 1);
    strncpy(dec2part, op2 + find_dec2 + 1, len2 - find_dec2 - 1);
    strncpy(int1part, op1 + 0, find_dec1);
    strncpy(int2part, op2 + 0, find_dec2);

    int res_decpart[1001] = {0};

    if (len1 - find_dec1 < len2 - find_dec2)
    {
        int j = 0, k = 0;
        int dec_num1[1001] = {0}, dec_num2[1001] = {0};

        // 先把字符数组转化为Int数组
        // 把多余的地方填充为0;
        for (int i = len2 - find_dec2 - 1; i > len1 - find_dec1 - 1; i--)
        {
            dec_num1[j] = 0;
            j++;
        }

        for (int i = len1 - find_dec1 - 2; i >= 0; i--)
        {
            dec_num1[j] = dec1part[i] - '0';
            if (dec_num1[j] > 9 || dec_num1[j] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            j++;
        }
        for (int i = len2 - find_dec2 - 2; i >= 0; i--)
        {
            dec_num2[k] = dec2part[i] - '0';
            if (dec_num2[k] > 9 || dec_num2[k] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            k++;
        }
        // 这里开始进行小数部分
        int carry = 0;
        int maxSize = len2 - find_dec2 - 1;
        // 这里多留了一位，用来处理有可能最后有进位
        int m = 0;
        int d = 0, l = 0;
        // 这里表示进位的操作，将余数存进答案数组，进位存进carry直到数组原数组遍历完
        while (d < len2 - find_dec2 - 1 || l < len2 - find_dec2 - 1)
        {
            int sum = carry;
            if (d < len2 - find_dec2 - 1)
                sum += dec_num1[d++];
            if (l < len2 - find_dec2 - 1)
                sum += dec_num2[l++];
            res_decpart[m++] = sum % 10;
            carry = sum / 10;
        }
        res_decpart[maxSize] = carry;

        int s = 0, t = 0;
        int Int_num1[1001] = {0}, Int_num2[1001] = {0};

        // 把字符数组转化为Int数组
        for (int i = find_dec1 - 1; i >= 0; i--)
        {
            Int_num1[s] = int1part[i] - '0';
            if (Int_num1[s] > 9 || Int_num1[s] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            s++;
        }
        for (int i = find_dec2 - 1; i >= 0; i--)
        {
            Int_num2[t] = int2part[i] - '0';
            if (Int_num2[t] > 9 || Int_num2[t] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            t++;
        }

        int size = find_dec1;
        for (int i = 0; i < size; i++)
        {
            int sum = Int_num1[i] + carry;
            Int_num1[i] = sum % 10;
            carry = sum / 10;
        }
        // 如果最高位有进位，则需要将进位添加到结果数组的最高位
        if (carry > 0)
        {
            for (int i = size; i > 0; --i)
            {
                Int_num1[i] = Int_num1[i - 1];
            }
            Int_num1[size + 1] = carry;
            size = size + 1;
        }

        Integer_add(Int_num1, Int_num2, size, find_dec2);
        printf(".");
        for (int i = maxSize - 1; i >= 0; i--)
            printf("%d", res_decpart[i]);
    }

    else
    {
        int j = 0, k = 0;
        int dec_num1[1001] = {0}, dec_num2[1001] = {0};
        // 同理，也是先把字符数组转化为Int数组
        // 把多余的地方填充为0;
        for (int i = len1 - find_dec1 - 1; i > len2 - find_dec2 - 1; i--)
        {
            dec_num2[j] = 0;
            k++;
        }
        for (int i = len1 - find_dec1 - 2; i >= 0; i--)
        {
            dec_num1[j] = dec1part[i] - '0';
            if (dec_num1[j] > 9 || dec_num1[j] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            j++;
        }
        for (int i = len2 - find_dec2 - 2; i >= 0; i--)
        {
            dec_num2[k] = dec2part[i] - '0';
            if (dec_num2[k] > 9 || dec_num2[k] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            k++;
        }
        // 这里开始进行小数部分
        int carry = 0;
        int maxSize = len1 - find_dec1 - 1;
        // 这里多留了一位，用来处理有可能最后有进位
        int m = 0;
        int d = 0, l = 0;
        // 这里表示进位的操作，将余数存进答案数组，进位存进carry直到数组原数组遍历完
        while (d < len1 - find_dec1 - 1 || l < len1 - find_dec1 - 1)
        {
            int sum = carry;
            if (d < len1 - find_dec1 - 1)
                sum += dec_num1[d++];
            if (l < len1 - find_dec1 - 1)
                sum += dec_num2[l++];
            res_decpart[m++] = sum % 10;
            carry = sum / 10;
        }
        res_decpart[maxSize] = carry;

        int s = 0, t = 0;
        int Int_num1[1001] = {0}, Int_num2[1001] = {0};

        // 把字符数组转化为Int数组
        for (int i = find_dec1 - 1; i >= 0; i--)
        {
            Int_num1[s] = int1part[i] - '0';
            if (Int_num1[s] > 9 || Int_num1[s] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            s++;
        }
        for (int i = find_dec2 - 1; i >= 0; i--)
        {
            Int_num2[t] = int2part[i] - '0';
            if (Int_num2[t] > 9 || Int_num2[t] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            t++;
        }

        int size = find_dec1;
        for (int i = 0; i < size; i++)
        {
            int sum = Int_num1[i] + carry;
            Int_num1[i] = sum % 10;
            carry = sum / 10;
        }
        // 如果最高位有进位，则需要将进位添加到结果数组的最高位
        if (carry > 0)
        {
            for (int i = size; i > 0; --i)
            {
                Int_num1[i] = Int_num1[i - 1];
            }
            Int_num1[size + 1] = carry;
            size = size + 1;
        }

        Integer_add(Int_num1, Int_num2, size, find_dec2);
        printf(".");
        for (int i = maxSize - 1; i >= 0; i--)
            printf("%d", res_decpart[i]);
    }
}

void Decimal_substract(char op1[], char op2[], int len1, int len2)
{
    int find_dec1 = find_decimalpoint(op1, len1);
    int find_dec2 = find_decimalpoint(op2, len2);

    int find_sci1 = find_sci(op1, len1);
    int find_sci2 = find_sci(op2, len2);

    char newop1[1001] = {0}, newop2[1001] = {0};

    int tomovedecimal = len1 - 1 - find_dec1 > len2 - 1 - find_dec2 ? len1 - 1 - find_dec1 : len2 - 1 - find_dec2;

    // 这里把所有的小数都通过移动小数点位置变成乘法。
    // 同时更新最新op的长度。
    if (tomovedecimal == len1 - 1 - find_dec1)
    {
        // 注意去掉前面可能出现的0
        int start = 0, begin = 0;
        int j = 0, k = 0;

        for (start = 0; start < len1; start++)
        {
            if (op1[start] != '0' && op1[start] != '.')
                break;
        }
        for (int i = start; i < len1; i++)
        {
            if (i != find_dec1)
            {
                newop1[j++] = op1[i];
            }
        }

        for (begin = 0; begin < len2; begin++)
        {
            if (op2[begin] != '0' && op2[begin] != '.')
                break;
        }
        for (int i = begin; i < len2; i++)
        {
            if (i != find_dec2)
            {
                newop2[k++] = op2[i];
            }
        }
        for (int i = 0; i < ((len1 - find_dec1) - (len2 - find_dec2)); i++)
        {
            newop2[k++] = '0';
        }
        len1 = j;
        len2 = k;
    }
    else
    {
        int start = 0, begin = 0;
        int j = 0, k = 0;

        for (start = 0; start < len2; start++)
        {
            if (op2[start] != '0' && op2[start] != '.')
                break;
        }
        for (int i = start; i < len2; i++)
        {
            if (i != find_dec2)
            {
                newop2[j++] = op2[i];
            }
        }

        for (begin = 0; begin < len1; begin++)
        {
            if (op1[begin] != '0' && op1[begin] != '.')
                break;
        }
        for (int i = begin; i < len1; i++)
        {
            if (i != find_dec1)
            {
                newop1[k++] = op1[i];
            }
        }
        for (int i = 0; i < ((len2 - find_dec2) - (len1 - find_dec1)); i++)
        {
            newop1[k++] = '0';
        }
        len1 = k;
        len2 = j;
    }

    // 这里同理进行整数的减法
    int is_neg = 0;
    int len = 0;
    int a[1001] = {0}, b[1001] = {0};
    // 判断哪个字符串比较大
    if (len1 < len2 || (strcmp(op1, op2) < 0 && len1 == len2))
    {
        is_neg = 1;
        for (int i = len2 - 1; i >= 0; i--)
            a[len2 - i - 1] = newop2[i] - '0';
        for (int i = len1 - 1; i >= 0; i--)
            b[len1 - i - 1] = newop1[i] - '0';
    }
    else
    {
        for (int i = len1 - 1; i >= 0; i--)
            a[len1 - i - 1] = newop1[i] - '0';
        for (int i = len2 - 1; i >= 0; i--)
            b[len2 - i - 1] = newop2[i] - '0';
    }
    if (len1 > len2)
        len = len1;
    else
        len = len2;
    for (int i = 0; i < len; i++)
    {
        a[i] = a[i] - b[i];
        if (a[i] < 0)
        {
            a[i + 1] -= 1;
            a[i] += 10;
        }
    }

    while (a[len - 1] == 0 && len > 1)
        len--;
    if (is_neg == 1)
        printf("-");

    // 判断是否需要添加0
    if (tomovedecimal >= len)
    {
        printf("0.");
        for (int i = 0; i < (tomovedecimal - len); i++)
            printf("0");
        for (int i = len - 1; i >= 0; i--)
        {
            printf("%d", a[i]);
        }
    }

    else
    {
        for (int i = len - 1; i >= tomovedecimal; i--)
        {
            printf("%d", a[i]);
        }
        printf(".");
        for (int i = tomovedecimal - 1; i >= 0; i--)
        {
            printf("%d", a[i]);
        }
    }
}

void Decimal_multiply(char op1[], char op2[], int len1, int len2)
{
    // 对于含小数的乘法，思路是找到两个小数点的位置，然后其他的使用整数乘法，最后移动小数点的位置。
    // 科学计数法的指数位必须为整数..? 如果实现了小数的加减法可以进行拓展
    int find_dec1 = find_decimalpoint(op1, len1);
    int find_dec2 = find_decimalpoint(op2, len2);

    int find_sci1 = find_sci(op1, len1);
    int find_sci2 = find_sci(op2, len2);

    if (find_sci1 == len1 - 1 && find_sci2 == len2 - 1)
    {
        int len1 = strlen(op1);
        int len2 = strlen(op2);
        int maxSize = len1 > len2 ? len1 : len2;
        int j = 0, k = 0;
        int num1[1001] = {0}, num2[1001] = {0};
        // 把字符数组转化为Int数组,并且去除掉小数点
        for (int i = len1 - 1; i >= 0; i--)
        {
            if (op1[i] == '.')
            {
                continue;
            }
            num1[j] = op1[i] - '0';
            if (num1[j] > 9 || num1[j] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            j++;
        }
        for (int i = len2 - 1; i >= 0; i--)
        {
            if (op2[i] == '.')
            {
                continue;
            }
            num2[k] = op2[i] - '0';
            if (num2[k] > 9 || num2[k] < 0)
            {
                printf("The input cannot be interpret as numbers!");
                return;
            }
            k++;
        }
        int tomove = (len1 - find_dec1 - 1) + (len2 - find_dec2 - 1);
        Integer_multiply(num1, num2, j, k, tomove);
    }
    else
    {
        char normalpart1[1001] = {0}, normalpart2[1001] = {0};
        char scipart1[1001] = {0}, scipart2[1001] = {0};
        // 这里就是把有科学计数法和没有的部分分开，次方位置使用加法，e前面的乘数部分使用小数的乘法计算
        strncpy(scipart1, op1 + find_sci1 + 1, len1 - find_sci1 - 1);
        strncpy(scipart2, op2 + find_sci2 + 1, len2 - find_sci2 - 1);
        strncpy(normalpart1, op1 + 0, find_sci1);
        strncpy(normalpart2, op2 + 0, find_sci2);
        // 乘数部分进行小数乘法
        Decimal_multiply(normalpart1, normalpart2, find_sci1, find_sci2);
        printf("e");
        int newlen1 = len1 - find_sci1 - 1;
        int newlen2 = len2 - find_sci2 - 1;
        int *num1 = stringToArray_reverse(scipart1, &newlen1);
        int *num2 = stringToArray_reverse(scipart2, &newlen2);
        // 科学计数法进行加法
        Integer_add(num1, num2, newlen1, newlen2);
    }
}

void Decimal_division(char op1[], char op2[], int len1, int len2)
{
    int find_dec1 = find_decimalpoint(op1, len1);
    int find_dec2 = find_decimalpoint(op2, len2);

    int find_sci1 = find_sci(op1, len1);
    int find_sci2 = find_sci(op2, len2);
    if (find_sci1 == len1 - 1 && find_sci2 == len2 - 1)
    {
        // 这里检测两个小数点位数的差，作为最后商需要挪动小数点的位数。
        int tomove = (len2 - find_dec2 - 1) - (len1 - find_dec1 - 1);

        char newop1[1001] = {0};
        char newop2[1001] = {0};
        // 去除掉小数点传入新的数组并记录新数的字符串表示
        int tag1 = 0;
        int tag2 = 0;
        if (find_dec1 != len1 - 1)
        {
            int start = 0;
            for (int i = 0; i < len1; i++)
            {
                if (op1[i] != '.' && op1[i] != '0')
                {
                    start = i;
                    break;
                }
            }
            for (int i = start; i < len1; i++)
            {
                if (i != find_dec1)
                {
                    newop1[tag1++] = op1[i];
                }
            }
        }
        else
        {
            for (int i = 0; i < len1; i++)
            {
                newop1[tag1++] = op1[i];
            }
        }
        if (find_dec2 != len2 - 1)
        {
            int start = 0;
            for (int i = 0; i < len2; i++)
            {
                if (op2[i] != '.' && op2[i] != '0')
                {
                    start = i;
                    break;
                }
            }
            for (int i = start; i < len2; i++)
            {
                if (i != find_dec2)
                {
                    newop2[tag2++] = op2[i];
                }
            }
        }
        else
        {
            for (int i = 0; i < len2; i++)
            {
                newop2[tag2++] = op2[i];
            }
        }

        Integer_division(newop1, newop2, tag1, tag2, tomove);
    }

    else
    {
        char normalpart1[1001] = {0}, normalpart2[1001] = {0};
        char scipart1[1001] = {0}, scipart2[1001] = {0};
        // 这里同乘法，将科学计数法部分与普通乘数部分分开计算，分别进行减法和小数除法。
        strncpy(scipart1, op1 + find_sci1 + 1, len1 - find_sci1 - 1);
        strncpy(scipart2, op2 + find_sci2 + 1, len2 - find_sci2 - 1);
        strncpy(normalpart1, op1 + 0, find_sci1);
        strncpy(normalpart2, op2 + 0, find_sci2);
        Decimal_division(normalpart1, normalpart2, find_sci1, find_sci2);
        printf("e");
        Integer_subtract(scipart1, scipart2, len1 - find_sci1 - 1, len2 - find_sci2 - 1);
    }
}
// 此函数用来进行整数的计算
void integer_operation(char op1[], char operator, char op2[])
{
    int len1 = strlen(op1);
    int len2 = strlen(op2);
    int maxSize = len1 > len2 ? len1 : len2;
    char newop1[1001] = {0}, newop2[1001] = {0};

    switch (operator)
    {
    // 这里直接判断存在负数直接的加减乘除，如果存在，就判断不同类型就直接跳转到相应的计算方法（比如加法中整数加负数，就直接化成正数之间的减法运算）
    case '+':
        printf("%s %c %s = ", op1, operator, op2);
        if (op1[0] == '-' && op2[0] == '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len1 = len1 - 1;
            len2 = len2 - 1;
            int *num1 = stringToArray_reverse(newop1, &len1);
            int *num2 = stringToArray_reverse(newop2, &len2);
            printf("-");
            Integer_add(num1, num2, len1, len2);
        }
        else if (op1[0] == '-' && op2[0] != '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            len1 = len1 - 1;
            Integer_subtract(op2, newop1, len2, len1);
        }
        else if (op1[0] != '-' && op2[0] == '-')
        {
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len2 = len2 - 1;
            Integer_subtract(op1, newop2, len1, len2);
        }
        else
        {
            int *num1 = stringToArray_reverse(op1, &len1);
            int *num2 = stringToArray_reverse(op2, &len2);
            Integer_add(num1, num2, len1, len2);
        }
        printf("\n");
        break;
    case '-':
        printf("%s %c %s = ", op1, operator, op2);
        if (op1[0] == '-' && op2[0] == '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len1 = len1 - 1;
            len2 = len2 - 1;
            Integer_subtract(newop2, newop1, len2, len1);
        }
        else if (op1[0] == '-' && op2[0] != '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            len1 = len1 - 1;
            int *num1 = stringToArray_reverse(newop1, &len1);
            int *num2 = stringToArray_reverse(op2, &len2);
            printf("-");
            Integer_add(num1, num2, len1, len2);
        }
        else if (op1[0] != '-' && op2[0] == '-')
        {
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len2 = len2 - 1;
            int *num1 = stringToArray_reverse(op1, &len1);
            int *num2 = stringToArray_reverse(newop2, &len2);
            Integer_add(num1, num2, len1, len2);
        }
        else
        {
            Integer_subtract(op1, op2, len1, len2);
        }
        printf("\n");
        break;
    case '*':
        printf("%s %c %s = ", op1, operator, op2);
        // 分情况完成去符号操作
        if (op1[0] == '-' && op2[0] == '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len1 = len1 - 1;
            len2 = len2 - 1;
        }
        else if (op1[0] == '-' && op2[0] != '-')
        {
            for (int i = 1; i < len1; i++)
                newop1[i - 1] = op1[i];
            for (int i = 0; i < len2; i++)
                newop2[i] = op2[i];
            len1 = len1 - 1;
            printf("-");
        }
        else if (op2[0] == '-' && op1[0] != '-')
        {
            for (int i = 1; i < len2; i++)
                newop2[i - 1] = op2[i];
            for (int i = 0; i < len1; i++)
                newop1[i] = op1[i];
            len2 = len2 - 1;
            printf("-");
        }
        else
        {
            for (int i = 0; i < len2; i++)
                newop2[i] = op2[i];
            for (int i = 0; i < len1; i++)
                newop1[i] = op1[i];
        }
        int *num1 = stringToArray_reverse(newop1, &len1);
        int *num2 = stringToArray_reverse(newop2, &len2);
        Integer_multiply(num1, num2, len1, len2, 0);
        printf("\n");
        break;
    case '/':
        if (!strcmp(op2, "0"))
            printf("A number cannot be divied by zero!\n");
        else
        {
            printf("%s %c %s = ", op1, operator, op2);
            if (op1[0] == '-' && op2[0] == '-')
            {
                for (int i = 1; i < len1; i++)
                {
                    newop1[i - 1] = op1[i];
                }
                for (int i = 1; i < len2; i++)
                {
                    newop2[i - 1] = op2[i];
                }
                len1 = len1 - 1;
                len2 = len2 - 1;
            }
            else if (op1[0] == '-' && op2[0] != '-')
            {
                for (int i = 1; i < len1; i++)
                    newop1[i - 1] = op1[i];
                for (int i = 0; i < len2; i++)
                    newop2[i] = op2[i];
                len1 = len1 - 1;
                printf("-");
            }
            else if (op2[0] == '-' && op1[0] != '-')
            {
                for (int i = 1; i < len2; i++)
                    newop2[i - 1] = op2[i];
                for (int i = 0; i < len1; i++)
                    newop1[i] = op1[i];
                len2 = len2 - 1;
                printf("-");
            }
            else
            {
                for (int i = 0; i < len2; i++)
                    newop2[i] = op2[i];
                for (int i = 0; i < len1; i++)
                    newop1[i] = op1[i];
            }
            Integer_division(newop1, newop2, len1, len2, 0);
            printf("\n");
            break;
        default:
            printf("Your operator input cannot be interpreted!\n");
            break;
        }
    }
}
// 此函数用来进行带有小数的计算
void decimal_operation(char *op1, char operator, char * op2)
{
    int len1 = strlen(op1);
    int len2 = strlen(op2);
    int maxSize = len1 > len2 ? len1 : len2;
    char newop1[1001] = {0}, newop2[1001] = {0};

    switch (operator)
    {
    // 小数计算的时候同整数一样，直接进行计算分类，化成正数之间的计算。
    case '+':
        printf("%s %c %s = ", op1, operator, op2);
        if (op1[0] == '-' && op2[0] == '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len1 = len1 - 1;
            len2 = len2 - 1;
            printf("-");
            Decimal_add(newop2, newop1, len2, len1);
        }
        else if (op1[0] == '-' && op2[0] != '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            len1 = len1 - 1;
            Decimal_substract(op2, newop1, len2, len1);
        }
        else if (op1[0] != '-' && op2[0] == '-')
        {
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len2 = len2 - 1;
            Decimal_substract(op1, newop2, len1, len2);
        }
        else
        {
            Decimal_add(op1, op2, len1, len2);
        }
        printf("\n");
        break;
    case '-':
        printf("%s %c %s = ", op1, operator, op2);
        if (op1[0] == '-' && op2[0] == '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len1 = len1 - 1;
            len2 = len2 - 1;
            Decimal_substract(newop2, newop1, len2, len1);
        }
        else if (op1[0] == '-' && op2[0] != '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            len1 = len1 - 1;
            printf("-");
            Decimal_add(op2, newop1, len2, len1);
        }
        else if (op1[0] != '-' && op2[0] == '-')
        {
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len2 = len2 - 1;
            Decimal_add(op1, newop2, len1, len2);
        }
        else
        {
            Decimal_substract(op1, op2, len1, len2);
        }
        printf("\n");
        break;
    case '*':
        printf("%s %c %s = ", op1, operator, op2);
        if (op1[0] == '-' && op2[0] == '-')
        {
            for (int i = 1; i < len1; i++)
            {
                newop1[i - 1] = op1[i];
            }
            for (int i = 1; i < len2; i++)
            {
                newop2[i - 1] = op2[i];
            }
            len1 = len1 - 1;
            len2 = len2 - 1;
        }
        else if (op1[0] == '-' && op2[0] != '-')
        {
            for (int i = 1; i < len1; i++)
                newop1[i - 1] = op1[i];
            for (int i = 0; i < len2; i++)
                newop2[i] = op2[i];
            len1 = len1 - 1;
            printf("-");
        }
        else if (op2[0] == '-' && op1[0] != '-')
        {
            for (int i = 1; i < len2; i++)
                newop2[i - 1] = op2[i];
            for (int i = 0; i < len1; i++)
                newop1[i] = op1[i];
            len2 = len2 - 1;
            printf("-");
        }
        else
        {
            for (int i = 0; i < len2; i++)
                newop2[i] = op2[i];
            for (int i = 0; i < len1; i++)
                newop1[i] = op1[i];
        }
        Decimal_multiply(newop1, newop2, len1, len2);
        printf("\n");
        break;
    case '/':
        if (!strcmp(op2, "0"))
            printf("A number cannot be divied by zero!\n");
        else
        {
            printf("%s %c %s = ", op1, operator, op2);
            if (op1[0] == '-' && op2[0] == '-')
            {
                for (int i = 1; i < len1; i++)
                {
                    newop1[i - 1] = op1[i];
                }
                for (int i = 1; i < len2; i++)
                {
                    newop2[i - 1] = op2[i];
                }
                len1 = len1 - 1;
                len2 = len2 - 1;
            }
            else if (op1[0] == '-' && op2[0] != '-')
            {
                for (int i = 1; i < len1; i++)
                    newop1[i - 1] = op1[i];
                for (int i = 0; i < len2; i++)
                    newop2[i] = op2[i];
                len1 = len1 - 1;
                printf("-");
            }
            else if (op2[0] == '-' && op1[0] != '-')
            {
                for (int i = 1; i < len2; i++)
                    newop2[i - 1] = op2[i];
                for (int i = 0; i < len1; i++)
                    newop1[i] = op1[i];
                len2 = len2 - 1;
                printf("-");
            }
            else
            {
                for (int i = 0; i < len2; i++)
                    newop2[i] = op2[i];
                for (int i = 0; i < len1; i++)
                    newop1[i] = op1[i];
            }
            Decimal_division(newop1, newop2, len1, len2);
            printf("\n");
            break;
        default:
            printf("Your operator input cannot be interpreted!\n");
            break;
        }
    }
}
// 此函数用来判断是否输入的是可以解释的数字
int judge_if_interpretable(char op[])
{
    int res = 1;
    int lens = strlen(op);
    for (int i = 0; i < lens; i++)
    {
        if (op[i] != 'e' && op[i] != '.' && !isdigit(op[i]))
        {
            res = 0;
            printf("The input cannot be interpret as numbers!Please try again!\n");
            return res;
        }
    }
}

int main(int argc, char *argv[])
{
    // 这里分类判断是不是一个命令行直接读入数据，否则就是一个多输入计算的模式
    if (argc == 1)
    {
        char op1[101], op2[101], operator;
        while (1)
        {
            printf("(Please Type quit to terminate)Enter operand 1:");
            scanf("%s", op1);

            if (strcmp(op1, "quit") == 0)
                break;

            printf("Enter operator: ");
            scanf(" %c", &operator);

            printf("Enter operand 2: ");
            scanf("%s", op2);

            if (judge_if_interpretable(op1) && judge_if_interpretable(op2))
            {
                if (strchr(op1, '.') == NULL && strchr(op2, '.') == NULL)
                {
                    // 整数运算
                    integer_operation(op1, operator, op2);
                }
                else
                {
                    // 小数运算
                    decimal_operation(op1, operator, op2);
                }
            }
        }
    }
    else
    {
        char oper;
        if (strcmp(argv[2], "+") == 0)
            oper = '+';
        // 由于'*'属于通配符,所以在命令行输入时候需要输入'*'。
        else if (strcmp(argv[2], "*") == 0)
            oper = '*';
        else if (strcmp(argv[2], "-") == 0)
            oper = '-';
        else if (strcmp(argv[2], "/") == 0)
            oper = '/';

        if (judge_if_interpretable(argv[1]) && judge_if_interpretable(argv[1]))
        {
            if (strchr(argv[1], '.') == NULL && strchr(argv[3], '.') == NULL)
            {
                // 整数运算
                integer_operation(argv[1], oper, argv[3]);
            }
            else
            {
                // 小数运算
                decimal_operation(argv[1], oper, argv[3]);
            }
        }
    }
}