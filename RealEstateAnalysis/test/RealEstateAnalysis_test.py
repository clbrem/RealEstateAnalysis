from unittest import TestCase, skip
import RealEstateAnalysis
import warnings
from RealEstateAnalysis.Data import DataStream, DataCsv
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
		self.csv = DataCsv.new("RealEstateAnalysis/SampleData/EBR_Building_Permits.csv", "latin-1")
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




	def test_canExport(self):
		self.csv.reset()
		self.csv.process(geolocation = self.parseGeo)
		self.csv.load()
		sample = self.csv.sample(10)
		output = sample.export(['geolocation', 'project_value'])
		self.assertEqual(len(output),10)
		
	def test_deprecated(self):
		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter("always")
			self.csv.reset()
			self.csv.process(geolocation = self.parseGeo)
			self.assertGreaterEqual(len(w), 1)
			self.assertTrue(issubclass(w[-1].category, DeprecationWarning ))
		warnings.simplefilter("default")

	def test_can_select(self):
		self.csv.reset()
		self.csv.select(geolocation = lambda x: self.parseGeo(x['geolocation']), project_value=lambda x: float(x['project_value'].replace('$','')))
		self.csv.load()
		first = self.csv[0]
		self.assertIn('geolocation', first)
		self.assertIn('project_value', first)
		self.assertEqual(len(first['geolocation']), 2)
		
	

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

	