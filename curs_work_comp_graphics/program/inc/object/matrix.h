#ifndef MATRIX_H
#define MATRIX_H

#include <cmath>
#include <cstring>
#include <memory>
#include <stdio.h>
#include "point.h"

template <typename T, size_t S>
class Matrix{
public:

    Matrix& operator =(const Matrix& m){
        memcpy(elements, m.elements, sizeof(elements));
        return *this;
    }

    Matrix operator *(const T& val) const{
        Matrix res = *this;
        for( auto& row : res.elements )
        {
            for( T& e : row )
            {
                e *= val;
            }
        }
        return res;
    }

    Matrix& operator *=(const T& val){
        *this = *this * val;
        return *this;
    }

    Matrix operator *(const Matrix& mat) const{
        Matrix result;
        for( size_t j = 0; j < S; j++ )
        {
            for( size_t k = 0; k < S; k++ )
            {
                T sum = (T)0.0;
                for( size_t i = 0; i < S; i++ )
                {
                    sum += elements[j][i] * mat.elements[i][k];
                }
                result.elements[j][k] = sum;
            }
        }
        return result;
    }

    Matrix& operator *=(const Matrix& mat){
        *this = *this * mat;
        return *this;
    }

    // транспонирование
    Matrix operator !() const{
        Matrix xp;
        for( size_t j = 0; j < S; j++ )
        {
            for( size_t k = 0; k < S; k++ )
            {
                xp.elements[j][k] = elements[k][j];
            }
        }
        return xp;
    }

    static Matrix Identity(){
        if (S == 3){
            return {
                (T)1.0,(T)0.0,(T)0.0,
                (T)0.0,(T)1.0,(T)0.0,
                (T)0.0,(T)0.0,(T)1.0,
            };
        } else if (S == 4){
            return {
                (T)1.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)1.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)1.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)1.0,
            };
        }
    }

    static Matrix Scaling(const T& factor_x, const T& factor_y, const T& factor_z){
        if (S == 3){
            return{
                factor_x,(T)0.0,(T)0.0,
                (T)0.0,factor_y,(T)0.0,
                (T)0.0,(T)0.0,factor_z,
            };
        } else if ( S == 4 ){
            return {
                factor_x,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,factor_y,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,factor_z,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)1.0,
            };
        }
    }

    static Matrix ScaleX(const T& factor){
        if (S == 3){
            return{
                factor,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,
            };
        } else if ( S == 4 ){
            return {
                factor,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)1.0,
            };
        }
    }


    static Matrix ScaleY(const T& factor){
        if (S == 3){
            return{
                (T)0.0,(T)0.0,(T)0.0,
                (T)0.0,factor,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,
            };
        } else if ( S == 4 ){
            return {
                (T)0.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,factor,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)1.0,
            };
        }
    }

    static Matrix ScaleZ(const T& factor){
        if (S == 3){
            return{
                (T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,factor,
            };
        } else if ( S == 4 ){
            return {
                (T)0.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,factor,(T)0.0,
                (T)0.0,(T)0.0,(T)0.0,(T)1.0,
            };
        }
    }

    static Matrix RotationZ(const T& theta){
        const T angle = theta * M_PI / (T)180;
        const T sinTheta = sin( angle );
        const T cosTheta = cos( angle );
        if ( S == 3 )
        {
            return{
                 cosTheta, sinTheta, (T)0.0,
                -sinTheta, cosTheta, (T)0.0,
                (T)0.0,    (T)0.0,   (T)1.0,
            };
        }
        else if ( S == 4 )
        {
            return {
                 cosTheta, sinTheta, (T)0.0,(T)0.0,
                -sinTheta, cosTheta, (T)0.0,(T)0.0,
                (T)0.0,    (T)0.0,   (T)1.0,(T)0.0,
                (T)0.0,	   (T)0.0,   (T)0.0,(T)1.0,
            };
        }
    }

    static Matrix RotationY(const T& theta){
        const T angle = theta * M_PI / (T)180;
        const T sinTheta = sin( angle );
        const T cosTheta = cos( angle );
        if ( S == 3 )
        {
            return{
                 cosTheta, (T)0.0,-sinTheta,
                 (T)0.0,   (T)1.0, (T)0.0,
                 sinTheta, (T)0.0, cosTheta
            };
        }
        else if ( S == 4 )
        {
            return {
                cosTheta, (T)0.0, -sinTheta,(T)0.0,
                (T)0.0,   (T)1.0, (T)0.0,   (T)0.0,
                sinTheta, (T)0.0, cosTheta, (T)0.0,
                (T)0.0,   (T)0.0, (T)0.0,   (T)1.0,
            };
        }
    }

    static Matrix RotationX(const T& theta){
        const T angle = theta * M_PI / (T)180;
        const T sinTheta = sin( angle );
        const T cosTheta = cos( angle );
        if ( S == 3 )
        {
            return{
                (T)1.0, (T)0.0,   (T)0.0,
                (T)0.0, cosTheta, sinTheta,
                (T)0.0,-sinTheta, cosTheta,
            };
        }
        else if ( S == 4 )
        {
            return {
                (T)1.0, (T)0.0,   (T)0.0,  (T)0.0,
                (T)0.0, cosTheta, sinTheta,(T)0.0,
                (T)0.0,-sinTheta, cosTheta,(T)0.0,
                (T)0.0, (T)0.0,   (T)0.0,  (T)1.0,
            };
        }
    }

    static Matrix Translation(T x, T y, T z){
        if ( S == 4 )
        {
            return {
                (T)1.0,(T)0.0,(T)0.0,(T)0.0,
                (T)0.0,(T)1.0,(T)0.0,(T)0.0,
                (T)0.0,(T)0.0,(T)1.0,(T)0.0,
                x,     y,      z,    (T)1.0,
            };
        }
    }

    static Matrix ProjectionFOV(T fov,T ar,T n,T f){
        if ( S == 4 ){
            const T fov_rad = fov * (T)M_PI / (T)180.0;
            const T yScale = (T)1.0 / (T)std::tan(fov_rad * (T)0.5);
            const T xScale = yScale / ar;
            return{
                xScale,  (T)0.0,  (T)0.0,				(T)0.0,
                (T)0.0,  yScale,	(T)0.0,				(T)0.0,
                (T)0.0,	 (T)0.0,	 (f / (f - n)),  (T)1.0,
                (T)0.0,	 (T)0.0,	 (-(f * n) / (f - n)),	(T)0.0,
            };
        }
    }

    Matrix LookAtLH(const point position, const point at, const point up){
        if  (S == 4){
            auto zaxis = (at - position).normalize();
            auto xaxis = (point::cross(up, zaxis)).normalize();
            auto yaxis = point::cross(zaxis, xaxis);
            return {
                xaxis.get_x(),  yaxis.get_x(), zaxis.get_x(), (T)0,
                xaxis.get_y(),  yaxis.get_y(), zaxis.get_y(), (T)0,
                xaxis.get_z(),  yaxis.get_z(), zaxis.get_z(), (T)0,
                -point::dot(xaxis, position), -point::dot(yaxis, position), -point::dot(zaxis, position) , (T)1
            };
        }
    }

    static Matrix RotationMatrix(point p, float angle){
        if (S == 4){
            angle = angle * (T)M_PI / (T)180.0;
            float sin = std::sin(angle), cos = std::cos(angle);
            return {
            cos+p.get_x()*p.get_x()*(1-cos), p.get_x()*p.get_y()*(1.f-cos)-p.get_z()*sin,
            p.get_x()*p.get_z()*(1.f-cos)+p.get_y()*sin, (T)0,
            p.get_y()*p.get_x()*(1.f-cos)+p.get_z()*sin,  cos+p.get_y()*p.get_y()*(1.f-cos),
            p.get_y()*p.get_z()*(1.f-cos)-p.get_x()*sin, (T)0,
            p.get_z()*p.get_x()*(1.f-cos)-p.get_y()*sin, p.get_z()*p.get_y()*(1.f-cos)+p.get_x()*sin,
            cos+p.get_z()*p.get_z()*(1.f-cos),  (T)0, (T)0, (T)0, (T)0, (T)1
        };
        }
    }

    static Matrix Inverse(const Matrix& m){
        if (S == 4){
            double Result[4][4];
            double tmp[12]; /* temp array for pairs */
            double src[16]; /* array of transpose source matrix */
            double det; /* determinant */
            /* transpose matrix */
            for (int i = 0; i < 4; i++)
            {
                src[i + 0 ] = m.elements[i][0];
                src[i + 4 ] = m.elements[i][1];
                src[i + 8 ] = m.elements[i][2];
                src[i + 12] = m.elements[i][3];
            }
            /* calculate pairs for first 8 elements (cofactors) */
            tmp[0] = src[10] * src[15];
            tmp[1] = src[11] * src[14];
            tmp[2] = src[9] * src[15];
            tmp[3] = src[11] * src[13];
            tmp[4] = src[9] * src[14];
            tmp[5] = src[10] * src[13];
            tmp[6] = src[8] * src[15];
            tmp[7] = src[11] * src[12];
            tmp[8] = src[8] * src[14];
            tmp[9] = src[10] * src[12];
            tmp[10] = src[8] * src[13];
            tmp[11] = src[9] * src[12];

            Result[0][0] = tmp[0]*src[5] + tmp[3]*src[6] + tmp[4]*src[7];
            Result[0][0] -= tmp[1]*src[5] + tmp[2]*src[6] + tmp[5]*src[7];
            Result[0][1] = tmp[1]*src[4] + tmp[6]*src[6] + tmp[9]*src[7];
            Result[0][1] -= tmp[0]*src[4] + tmp[7]*src[6] + tmp[8]*src[7];
            Result[0][2] = tmp[2]*src[4] + tmp[7]*src[5] + tmp[10]*src[7];
            Result[0][2] -= tmp[3]*src[4] + tmp[6]*src[5] + tmp[11]*src[7];
            Result[0][3] = tmp[5]*src[4] + tmp[8]*src[5] + tmp[11]*src[6];
            Result[0][3] -= tmp[4]*src[4] + tmp[9]*src[5] + tmp[10]*src[6];
            Result[1][0] = tmp[1]*src[1] + tmp[2]*src[2] + tmp[5]*src[3];
            Result[1][0] -= tmp[0]*src[1] + tmp[3]*src[2] + tmp[4]*src[3];
            Result[1][1] = tmp[0]*src[0] + tmp[7]*src[2] + tmp[8]*src[3];
            Result[1][1] -= tmp[1]*src[0] + tmp[6]*src[2] + tmp[9]*src[3];
            Result[1][2] = tmp[3]*src[0] + tmp[6]*src[1] + tmp[11]*src[3];
            Result[1][2] -= tmp[2]*src[0] + tmp[7]*src[1] + tmp[10]*src[3];
            Result[1][3] = tmp[4]*src[0] + tmp[9]*src[1] + tmp[10]*src[2];
            Result[1][3] -= tmp[5]*src[0] + tmp[8]*src[1] + tmp[11]*src[2];

            tmp[0] = src[2]*src[7];
            tmp[1] = src[3]*src[6];
            tmp[2] = src[1]*src[7];
            tmp[3] = src[3]*src[5];
            tmp[4] = src[1]*src[6];
            tmp[5] = src[2]*src[5];

            tmp[6] = src[0]*src[7];
            tmp[7] = src[3]*src[4];
            tmp[8] = src[0]*src[6];
            tmp[9] = src[2]*src[4];
            tmp[10] = src[0]*src[5];
            tmp[11] = src[1]*src[4];

            Result[2][0] = tmp[0]*src[13] + tmp[3]*src[14] + tmp[4]*src[15];
            Result[2][0] -= tmp[1]*src[13] + tmp[2]*src[14] + tmp[5]*src[15];
            Result[2][1] = tmp[1]*src[12] + tmp[6]*src[14] + tmp[9]*src[15];
            Result[2][1] -= tmp[0]*src[12] + tmp[7]*src[14] + tmp[8]*src[15];
            Result[2][2] = tmp[2]*src[12] + tmp[7]*src[13] + tmp[10]*src[15];
            Result[2][2] -= tmp[3]*src[12] + tmp[6]*src[13] + tmp[11]*src[15];
            Result[2][3] = tmp[5]*src[12] + tmp[8]*src[13] + tmp[11]*src[14];
            Result[2][3] -= tmp[4]*src[12] + tmp[9]*src[13] + tmp[10]*src[14];
            Result[3][0] = tmp[2]*src[10] + tmp[5]*src[11] + tmp[1]*src[9];
            Result[3][0] -= tmp[4]*src[11] + tmp[0]*src[9] + tmp[3]*src[10];
            Result[3][1] = tmp[8]*src[11] + tmp[0]*src[8] + tmp[7]*src[10];
            Result[3][1] -= tmp[6]*src[10] + tmp[9]*src[11] + tmp[1]*src[8];
            Result[3][2] = tmp[6]*src[9] + tmp[11]*src[11] + tmp[3]*src[8];
            Result[3][2] -= tmp[10]*src[11] + tmp[2]*src[8] + tmp[7]*src[9];
            Result[3][3] = tmp[10]*src[10] + tmp[4]*src[8] + tmp[9]*src[9];
            Result[3][3] -= tmp[8]*src[9] + tmp[11]*src[10] + tmp[5]*src[8];

            det=src[0]*Result[0][0]+src[1]*Result[0][1]+src[2]*Result[0][2]+src[3]*Result[0][3];
            det = 1.0f / det;

            Matrix res;
            for (int i = 0; i < 4; i++)
            {
                for (int j = 0; j < 4; j++)
                {
                    res.elements[i][j] = T(Result[i][j] * det);
                }
            }
            return res;
        }

    }

public:
    T elements[S][S];
};


template<typename T>
point & operator *=(point & l, const Matrix<T, 3>& r){
    return l = l * r;
}

template<typename T>
point operator *(const point & lhs, const Matrix<T,3>& rhs){
    return{
        lhs.get_x() * rhs.elements[0][0] + lhs.get_y() * rhs.elements[1][0] + lhs.get_z() * rhs.elements[2][0],
        lhs.get_x() * rhs.elements[0][1] + lhs.get_y() * rhs.elements[1][1] + lhs.get_z() * rhs.elements[2][1],
        lhs.get_x() * rhs.elements[0][2] + lhs.get_y() * rhs.elements[1][2] + lhs.get_z() * rhs.elements[2][2]
    };
}

template <typename T>
point& operator *=(const point& lhs, const Matrix<T, 4>& rhs){
    return lhs = lhs * rhs;
}

template <typename T>
point4 operator *(const point4& lhs, const Matrix<T, 4>& rhs){
    return{
        lhs.get_x() * rhs.elements[0][0] + lhs.get_y() * rhs.elements[1][0] + lhs.get_z() * rhs.elements[2][0] + lhs.get_f() * rhs.elements[3][0],
        lhs.get_x() * rhs.elements[0][1] + lhs.get_y() * rhs.elements[1][1] + lhs.get_z() * rhs.elements[2][1] + lhs.get_f() * rhs.elements[3][1],
        lhs.get_x() * rhs.elements[0][2] + lhs.get_y() * rhs.elements[1][2] + lhs.get_z() * rhs.elements[2][2] + lhs.get_f() * rhs.elements[3][2],
        lhs.get_x() * rhs.elements[0][3] + lhs.get_y() * rhs.elements[1][3] + lhs.get_z() * rhs.elements[2][3] + lhs.get_f() * rhs.elements[3][3]
    };

}

using Mat3x3f = Matrix<float, 3>;
using Mat3x3d = Matrix<double, 3>;
using Mat4x4f = Matrix<float, 4>;
using Mat4x4d = Matrix<double, 4>;

#endif
