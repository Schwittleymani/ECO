import gensim
import math

def buildWord2Vec(sentenceFile, modelFile):

	model = gensim.models.Word2Vec(sentenceFile, window = 7, workers=8)
	model.init_sims(replace=True)
	print model
	print 'model memory size, mb:', model.estimate_memory()['total']/(math.pow(1024,2))
	model.save(modelFile)


def process_arguments(args):
    parser = argparse.ArgumentParser(description='configure Word2Vec model building')
    parser.add_argument('--inputfile', action='store', help='the path to a folder containing sentence txt file')
    parser.add_argument('--outputfile', action='store', help='the path to the final model')


if __name__ == '__main__':
	params = process_arguments(sys.argv[1:])
	buildWord2Vec(params['inputfile'],params['outputfile'])