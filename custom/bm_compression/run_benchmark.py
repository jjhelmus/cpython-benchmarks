import bz2
import lzma
import time
from string import printable


import pyperf

SMALL_DATA = printable.encode() * 2**8
LARGE_DATA = printable.encode() * 2**12


def _bench_decompress(loops, decompressor, data):
    range_it = range(loops)
    t0 = time.perf_counter()
    for _ in range_it:
        decompressor.decompress(data)
    return time.perf_counter() - t0


def bench_bz2_decompress_small(loops):
    return _bench_decompress(loops, bz2, bz2.compress(SMALL_DATA))


def bench_bz2_decompress_large(loops):
    return _bench_decompress(loops, bz2, bz2.compress(LARGE_DATA))


def bench_lzma_decompress_small(loops):
    return _bench_decompress(loops, lzma, lzma.compress(SMALL_DATA))


def bench_lzma_decompress_large(loops):
    return _bench_decompress(loops, lzma, lzma.compress(LARGE_DATA))


def _bench_compress(loops, compressor, data):
    range_it = range(loops)
    t0 = time.perf_counter()
    for _ in range_it:
        compressor.compress(data)
    compressor.flush()
    return time.perf_counter() - t0


def bench_bz2_compress_small(loops):
    return _bench_compress(loops, bz2.BZ2Compressor(), SMALL_DATA)


def bench_bz2_compress_large(loops):
    return _bench_compress(loops, bz2.BZ2Compressor(), LARGE_DATA)


def bench_lzma_compress_small(loops):
    return _bench_compress(loops, lzma.LZMACompressor(), SMALL_DATA)


def bench_lzma_compress_large(loops):
    return _bench_compress(loops, lzma.LZMACompressor(), LARGE_DATA)


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata["description"] = "compression benchmarks"

    args = runner.parse_args()

    runner.bench_time_func("bz2_compress_small", bench_bz2_compress_small)
    runner.bench_time_func("bz2_compress_large", bench_bz2_compress_large)

    runner.bench_time_func("lzma_compress_small", bench_lzma_compress_small)
    runner.bench_time_func("lzma_compress_large", bench_lzma_compress_large)

    runner.bench_time_func("bz2_decompress_small", bench_bz2_decompress_small)
    runner.bench_time_func("bz2_decompress_large", bench_bz2_decompress_large)

    runner.bench_time_func("lzma_decompress_small", bench_lzma_decompress_small)
    runner.bench_time_func("lzma_decompress_large", bench_lzma_decompress_large)
