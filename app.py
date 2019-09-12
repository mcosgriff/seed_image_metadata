from PIL import Image
from PIL.TiffTags import TAGS
import json
import os.path
import logging
import sys
from glob import glob


def runAlgorithm(tiff_path: str, output_dir: str) -> int:
    try:
        tiff_basename = os.path.basename(tiff_path)
        out_file_path = os.path.join(
            output_dir, tiff_basename.replace('.tif', '_metadata.json'))

        with Image.open(tiff_path) as img:
            meta_dict = {TAGS[key]: img.tag[key] for key in img.tag.keys()}

            with open(out_file_path, mode='w') as fp:
                json.dump(meta_dict, fp, indent=4)
                log.info('Wrote output to {}'.format(out_file_path))

        log.info('Returning from algorithm...')
    except:
        return os.EX_IOERR

    return os.EX_OK


def generateResultsManifest(output_dir: str):
    try:
        output_log = glob(os.path.join(output_dir, '*_metadata.json'))[0]
    except:
        log.exception('Error in locating output files')
        sys.exit(10)

    if not output_log:
        log.error('No outputs found in directory for manifest')
        sys.exit(11)

    json_dict = {}
    json_dict['version'] = '1.1'
    json_dict['output_data'] = []

    temp_dict = {}
    temp_dict['name'] = 'metadata'
    temp_dict['file'] = {'path': output_log}
    json_dict['output_data'].append(temp_dict)

    with open(os.path.join(output_dir, 'results_manifest.json'), mode='w') as fp:
        json.dump(json_dict, fp, indent=4)
        log.debug('Wrote manifest to {}'.format(os.path.join(output_dir, 'results_manifest.json')))

    log.info('Completed manifest creation')


if __name__ == "__main__":
    #Setup Logger to capture print statements
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    consoleFormatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(consoleFormatter)
    log.addHandler(consoleHandler)

    argv = sys.argv
    if argv is None:
        log.error('No inputs passed to algorithm')
        sys.exit(2)
    argc = len(argv) - 1

    tiff_path = argv[1]
    output_dir = argv[2]

    log.debug('Tiff path: {}'.format(tiff_path))
    log.debug('Output directory: {}'.format(output_dir))

    if os.path.exists(tiff_path) and os.path.isfile(tiff_path) and os.path.exists(output_dir) and os.path.isdir(output_dir):
        exit_code = runAlgorithm(tiff_path, output_dir)

        if exit_code != 0:
            log.error('algorithm exited with code: {}'.format(exit_code))
        else:
            generateResultsManifest(output_dir)

        log.info('Completed Python Wrapper')

        sys.exit(exit_code)

    sys.exit(2)
