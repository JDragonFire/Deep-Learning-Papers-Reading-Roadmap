# pylint: disable=C0103,W1202,C0301,E501
"""
Merge PDF files

Run this file after downloading all pdfs

>>> python merge.py
"""
import argparse
import logging
import os
import subprocess
from typing import List

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def read_args() -> argparse.Namespace:
    """Reads command line arguments"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--dirname", default="pdfs", help="Directory that contains PDF files")
    parser.add_argument(
        "--n-batch",
        default=3,
        help="IF 2, divide all pdfs into two merged pdf files")

    parser.add_argument(
        "--target",
        default="all",
        help="Prefix filename for the merged PDF output")
    return parser.parse_args()


def get_all_pdf_paths(dirname: str) -> List[str]:
    """Return all PDF paths in DIRNAME

    Args:
        dirname (str): Directory that contains pdf files

    Returns:
        filenames (List[str]): A list of PDF paths.

    Example:
        >>> get_all_pdf_paths("pdfs")
        ["whatever.pdf", "inside.pdf", "pdfs_directory.pdf"]
    """
    result = []

    for parent, _, files in os.walk(dirname):
        for f in files:
            path = os.path.join(parent, f)
            if ".pdf" in path:
                result.append(path)

    return result


def build_pdftk_commands(filenames: List[str], destination: str) -> List[str]:
    """Returns a list of pdftk commands

    Args:
        filenames (List[str]): A list of filenames
        destination (str): Merged output filename

    Returns:
        List[str]: Shell Command to run pdftk

    Examples:
        >>> filenames = ["1.pdf", "2.pdf"]
        >>> destination = "merged.pdf"
        >>> build_pdftk_commands(filenames, destination)
        ["pdftk", "1.pdf", "2.pdf", "cat", "output", "merged.pdf"]
    """

    command = ["pdftk"]
    command.extend(filenames)

    command.extend(["cat", "output", destination])

    return command


def main(flags: argparse.Namespace) -> None:
    """Main Function"""
    pdfs = get_all_pdf_paths(flags.dirname)
    pdfs = sorted(pdfs)

    n_files = len(pdfs)

    batch_size = n_files // flags.n_batch
    index = 0

    LOGGER.info(f"Number of merged pdf files: {flags.n_batch}")
    LOGGER.info(f"Batch Size: {batch_size}")

    for i in range(0, n_files, batch_size):
        targets = pdfs[i:i + batch_size]
        cmd = build_pdftk_commands(targets, f"{flags.target}_{index}.pdf")

        LOGGER.info(f"Running {cmd[0]} {len(cmd[1:-3])} pdfs {cmd[-3:]}")
        subprocess.run(cmd)
        index += 1


if __name__ == '__main__':
    main(read_args())
