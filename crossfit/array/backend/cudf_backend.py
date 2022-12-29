import logging

from crossfit.array import conversion
from crossfit.array.dispatch import np_backend_dispatch, NPBackend


@np_backend_dispatch.register_lazy("cudf")
def register_cupy_backend():
    import cudf

    class CudfBackend(NPBackend):
        def __init__(self):
            super().__init__(cudf)

    np_backend_dispatch.register(cudf.Series)(CudfBackend())


@conversion.dispatch_to_dlpack.register_lazy("cudf")
def register_cudf_to_dlpack():
    import cudf

    @conversion.dispatch_to_dlpack.register(cudf.Series)
    def cudf_to_dlpack(input_array: cudf.Series):
        logging.debug(f"Converting {input_array} to DLPack")
        return input_array.to_dlpack()


@conversion.dispatch_from_dlpack.register_lazy("cudf")
def register_cudf_from_dlpack():
    import cudf

    @conversion.dispatch_from_dlpack.register(cudf.Series)
    def cudf_from_dlpack(capsule) -> cudf.Series:
        logging.debug(f"Converting {capsule} to cudf.Series")
        return cudf.io.from_dlpack(capsule)


@conversion.dispatch_to_array.register_lazy("cudf")
def register_cudf_to_array():
    import cudf

    @conversion.dispatch_to_array.register(cudf.Series)
    def cudf_to_array(input_array: cudf.Series):
        logging.debug(f"Converting {input_array} to np.ndarray")
        return input_array.to_numpy()


@conversion.dispatch_from_array.register_lazy("cudf")
@conversion.dispatch_from_cuda_array.register_lazy("cudf")
def register_cudf_from_array():
    import cudf

    @conversion.dispatch_from_array.register(cudf.Series)
    @conversion.dispatch_from_cuda_array.register(cudf.Series)
    def cudf_from_array(array) -> cudf.Series:
        logging.debug(f"Converting {array} to cudf.Series")
        return cudf.Series(array)
