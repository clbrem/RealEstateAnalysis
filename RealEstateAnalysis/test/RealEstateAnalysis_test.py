from unittest import TestCase, skip
import RealEstateAnalysis
from RealEstateAnalysis.data import DataStream, DataCsv
class RealEstateAnalysisTest(TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	@skip("fails")
	def test_something(self):
		self.assertTrue(False)

class DataCsvTest(TestCase):
	def setUp(self):
		self.csv = DataCsv.new("/Users/cbremer/Projects/TensorFlow/RealEstateAnalysis/RealEstateAnalysis/EBR_Building_Permits.csv", "latin-1")
		self.csv.load()

	def tearDown(self):
		pass

	def parseGeo(self, coords):
		return coords.split("\n")[-1].replace("(", "").replace(")", "").split(",")	
		
	def test_canCreateCsv(self):
		pass

	def test_canGetLength(self):
		self.assertGreater(len(self.csv) ,0)
	
	def test_canFilter(self):
		self.csv.reset()
		self.csv.where(permit_number = "69797")
		self.csv.load()
		self.assertEqual(len(self.csv), 1)
	
	def test_canSample(self):
		N = len(self.csv)
		sample = self.csv.sample(10)
		self.assertEqual(len(sample), 10)
		self.assertEqual(len(self.csv), N-10)

	def test_canProcess(self):
		self.csv.reset()
		
		self.csv.process(geolocation = self.parseGeo)
		self.csv.load()
		sample = self.csv.sample(1)[0]
		a, b = sample["geolocation"]
		self.assertGreater(float(a), 0)
		self.assertGreater(0, float(b))

	def test_canExport(self):
		self.csv.reset()
		self.csv.process(geolocation = self.parseGeo)
		self.csv.load()
		sample = self.csv.sample(10)
		output = sample.export(['geolocation', 'project_value'])
		self.assertEqual(len(output),10)
		
	

@skip("offline")
class DataStreamTest(TestCase):
	@skip("offline")
	def setUp(self):
		self.stream = DataStream.new("https://data.brla.gov/resource/f3qw-nd5k.json")
		self.stream.load()
	
	def tearDown(self):
		pass
	

	def test_canGetData(self):
		self.assertNotEqual(len(self.stream),0)
	

	def test_canIterate(self):		
		L = [x for x in self.stream]
		self.assertEqual(len(L), len(self.stream))
	

	def test_canFilter(self):
		self.stream.where(zip = 70808)
		self.stream.load()
		for x in self.stream:
			if x['zip'] != 70808:
				self.fail
	

	def test_canSample(self):
		N = len(self.stream)
		a = self.stream.sample(9)
		self.assertEqual(len(a), 9)
		self.assertEqual(len(self.stream), N -9)

	