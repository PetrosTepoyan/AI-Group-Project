import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    start_dir = 'tests'  # replace with your directory name if different
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
