#include <pybind11/pybind11.h>
#include "cs.h"

namespace py = pybind11;

PYBIND11_MODULE(_cluster_shapley, m) {
	
	py::class_<cs::ClusterShapley>(m, "ClusterShapley")
		.def(py::init<>())
		.def("compute_distances", &cs::ClusterShapley::compute_distances)
		.def("__repr__",
			[](cs::ClusterShapley& a) {
				return "<class.ClusterShapley>";
			});
}