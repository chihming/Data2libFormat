import argparse, logging
from code.DataConverter import DataConverter

# Arguments
PARSER = argparse.ArgumentParser(description="Parameters for the script.",
                                 usage="python main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]")

PARSER.add_argument('-task', "--Task", default=None,
                    help="Specify the task. Options: 'csv2lib', 'csv2rel'")

# Header for splitting data
PARSER.add_argument('-labels', "--Labels", default=None,
                    help="Specify labels for splitting data")
PARSER.add_argument('-target', "--TargetColumn", type=int, default=None,
                    help="Target column for input data.")
PARSER.add_argument('-rtarget', "--RTargetColumn", type=int, default=None,
                    help="Target column for rlational data.")
PARSER.add_argument('-cat', "--CategoricalColumn", default=None,
                    help="Categorical columns for encoding.")
PARSER.add_argument('-num', "--NumericColumn", default=None,
                    help="Numeric column for encoding.")
PARSER.add_argument('-ratio', "--Ratio", default=None,
                    help="param for splitting data")

# files
PARSER.add_argument('-infile', "--InputFileName", default=None,
                    help="Input File Name")
PARSER.add_argument('-outfile', "--OutputFileName", default=None,
                    help="Output File Name")
PARSER.add_argument('-relfile', "--RelationalFileName", default=None,
                    help="Relational File Name")

PARSER.add_argument('-header', "--Header", type=int, default=None,
                    help="With header or not")
PARSER.add_argument('-sep', "--Separtor", default=None,
                    help="separtor for splitting data")
PARSER.add_argument('-msep', "--MutiLabelSepartor", default=None,
                    help="separtor for splitting multiple-labeled data")

# features
PARSER.add_argument('-his', "--History", action="store_true",
                    help="Add history feature.")
PARSER.add_argument('-usim', "--AddUserSimilarity", action="store_true",
                    help="Add user similarity feature.")
PARSER.add_argument('-msim', "--AddMovieSimilarity", action="store_true",
                    help="Add movie similarity feature.")
PARSER.add_argument('-genre', "--AddGenres", action="store_true",
                    help="Add movie genres feature.")

# model parameters
PARSER.add_argument('-alpha', "--alpha", type=float, default=0.5,
                    help="Parameter of cosine similarity.")
PARSER.add_argument('-topk', "--topk", type=int, default=10,
                    help="Get top-k similarities.")
PARSER.add_argument('-offset', "--Offset", default=None,
                    help="Encoding offset")

PARSER.set_defaults(argument_default=False)
CONFIG = PARSER.parse_args()
logging.basicConfig(format="[%(asctime)s] %(levelname)s\t%(message)s",
                    level=logging.DEBUG,
                    datefmt='%m/%d/%y %H:%M:%S')
logger = logging.getLogger( __name__ )


# ----------------------

def main():
    DC = DataConverter(logger)

    if CONFIG.Task == 'dsplit':
        dataout = DC.SplitData(infile=CONFIG.InputFileName,
                               target_column=CONFIG.TargetColumn,
                               sep=CONFIG.Separtor,
                               header=CONFIG.Header,
                               ratio=CONFIG.Ratio)

        for e, out in enumerate(dataout):
            logger.info("Output result to '%s'" % (CONFIG.OutputFileName[e]))
            file_out = open(CONFIG.OutputFileName[e], 'wb')
            file_out.write('\n'.join(out))
            file_out.close()

    elif CONFIG.Task == 'csv2lib':
        dataout = DC.CSVtoLib(infile=CONFIG.InputFileName,
                              target_column=CONFIG.TargetColumn,
                              sep=CONFIG.Separtor,
                              msep=CONFIG.MutiLabelSepartor,
                              offset=CONFIG.Offset,
                              header=CONFIG.Header,
                              labels=CONFIG.Labels,
                              c_columns=CONFIG.CategoricalColumn,
                              n_columns=CONFIG.NumericColumn)

        for e, out in enumerate(dataout):
            logger.info("Output result to '%s'" % (CONFIG.OutputFileName[e]))
            file_out = open(CONFIG.OutputFileName[e], 'wb')
            file_out.write('\n'.join(out))
            file_out.close()

    elif CONFIG.Task == 'csv2rel':
        dataout = DC.CSVtoRel(infile=CONFIG.InputFileName,
                                     relfile=CONFIG.RelationalFileName,
                                     target_column=CONFIG.TargetColumn,
                                     rtarget_column=CONFIG.RTargetColumn,
                                     sep=CONFIG.Separtor,
                                     msep=CONFIG.MutiLabelSepartor,
                                     offset=CONFIG.Offset,
                                     header=CONFIG.Header,
                                     labels=CONFIG.Labels,
                                     c_columns=CONFIG.CategoricalColumn,
                                     n_columns=CONFIG.NumericColumn)

        logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0]))
        file_out = open(CONFIG.OutputFileName[0], 'wb')
        file_out.write('\n'.join(dataout[0]))
        file_out.close()

        logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0] + '.train'))
        file_out = open(CONFIG.OutputFileName[0] + '.train', 'wb')
        file_out.write('\n'.join(dataout[1]))
        file_out.close()

        logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0] + '.test'))
        file_out = open(CONFIG.OutputFileName[0] + '.test', 'wb')
        file_out.write('\n'.join(dataout[2]))
        file_out.close()

    else:
        logger.error("Unknow Task")


# ----------------------

if __name__ == '__main__':
    """
    Check Arguments &&
    Start Task
    """

    logger.info("Arguments Check")

    if CONFIG.Task is not None:
        logger.info("Task: '%s'" % CONFIG.Task)
    else:
        logger.error("Please Specify the Task.")
        logger.error("Options: 'csv2lib', 'csv2rel'")
        exit()

    if CONFIG.InputFileName is not None:
        CONFIG.InputFileName = CONFIG.InputFileName.split(',')
        logger.info("Input File: %s" % (CONFIG.InputFileName))
    else:
        logger.error("Please specify input files splitted by ','")
        exit()

    if CONFIG.OutputFileName is not None:
        CONFIG.OutputFileName = CONFIG.OutputFileName.split(',')
        logger.info("Output File: %s" % (CONFIG.OutputFileName))
    else:
        logger.error("Please specify output files splitted by ','")
        exit()

    if CONFIG.Task == 'csv2rel':
        if CONFIG.RelationalFileName is not None:
            logger.info("Relational File: '%s'" % CONFIG.RelationalFileName)
        else:
            logger.error("Please specify corresponding relational data")
            exit()

        if CONFIG.RTargetColumn is not None:
            logger.info("Relational Target Column: '%d'" % (CONFIG.RTargetColumn))
        else:
            logger.warning("Default Relational Target Column: '0'")
            CONFIG.RTargetColumn = 0

    if CONFIG.TargetColumn is not None:
        logger.info("Target Column: '%d'" % (CONFIG.TargetColumn))
    else:
        logger.warning("Default Target Column: '0'")
        CONFIG.TargetColumn = 0

    if CONFIG.Header is not None:
        logger.info("Header: '%s'" % (CONFIG.Header))
    else:
        logger.warning("Default Header: '0'")
        CONFIG.Header = False

    if CONFIG.Separtor is not None:
        logger.info("Separtor: '%s'" % CONFIG.Separtor)
    else:
        logger.warning("Default Separtor: ','")
        CONFIG.Separtor = ','

    if CONFIG.Separtor is not None:
        logger.info("Multi-labeled Separtor: '%s'" % CONFIG.Separtor)
    else:
        logger.warning("No multi-labeled data")

    if CONFIG.CategoricalColumn is not None:
        logger.info("Categorical Columns: '%s'" % CONFIG.CategoricalColumn)
        CONFIG.CategoricalColumn = [ int(c) for c in CONFIG.CategoricalColumn.split(',') ]
    else:
        CONFIG.CategoricalColumn = []

    if CONFIG.NumericColumn is not None:
        logger.info("Numeric Columns: '%s'" % CONFIG.NumericColumn)
        CONFIG.NumericColumn = [ int(c) for c in CONFIG.NumericColumn.split(',') ]
    else:
        CONFIG.NumericColumn = []

    if CONFIG.Offset is not None:
        logger.info("Offset: '%s' (index starts from %s)" % (CONFIG.Offset, CONFIG.Offset))
    else:
        logger.info("Offset: '1' (index start from 0)")
        CONFIG.Offset = 1

    if CONFIG.Ratio is not None:
        CONFIG.Ratio = CONFIG.Ratio.split(',')
        logger.info("Ratio: '%s'" % (CONFIG.Ratio))
    else:
        logger.warning("Default ratio: '0.8,0.2,0.5'")
        CONFIG.Ratio = '0.8,0.2,0.5'.split(',')


    logger.info("Task Start")
    main()

