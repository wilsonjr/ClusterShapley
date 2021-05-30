// Author: Wilson Estécio Marcílio Júnior <wilson_jr@outlook.com>

/*
 *
 * Copyright (c) 2021, Wilson Estécio Marcílio Júnior (São Paulo State University)
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 1. Redistributions of source code must retain the above copyright
 *  notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *  notice, this list of conditions and the following disclaimer in the
 *  documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *  must display the following acknowledgement:
 *  This product includes software developed by the São Paulo State University.
 * 4. Neither the name of the São Paulo State University nor the names of
 *  its contributors may be used to endorse or promote products derived from
 *  this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY WILSON ESTÉCIO MARCÍLIO JÚNIOR ''AS IS'' AND ANY EXPRESS
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
 * EVENT SHALL WILSON ESTÉCIO MARCÍLIO JÚNIOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
 * BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
 * IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
 * OF SUCH DAMAGE.
 *
 */

#include "cs.h"

namespace py = pybind11;
using namespace std;


double cs::ClusterShapley::distance(const double* a, const double* b, size_t n) 
{

	double sum = 0.0;

	for( size_t i = 0; i < n; ++i ) {

		sum += (*(a+i) - *(b+i))*(*(a+i) - *(b+i));

	}

	return std::sqrt(sum);
}


py::array_t<double> cs::ClusterShapley::compute_distances(py::array_t<double> points, py::array_t<double> centroids)
{
	py::buffer_info bf_points = points.request();
	double* ptr_points = (double*) bf_points.ptr;

	py::buffer_info bf_centroids = centroids.request();
	double* ptr_centroids = (double*) bf_centroids.ptr;

	vector<vector<double>> distances(bf_points.shape[0], vector<double>(bf_centroids.shape[0], 0.0));

	#pragma omp parallel for 
	for( int i = 0; i < distances.size(); ++i ) {
		for( int j = 0; j < distances[0].size(); ++j ) {
			distances[i][j] = this->distance(ptr_points + i*bf_points.shape[1], ptr_centroids + j*bf_centroids.shape[1], bf_points.shape[1]);
		}
	}


	return py::cast(distances);
}