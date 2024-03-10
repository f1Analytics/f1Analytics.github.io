from data_engine.fetcher import Fetcher

class EngineBucket:
    def __init__(self, gp, year):
        self.gp = gp
        self.year = year
        self.fetcher = Fetcher()
        
class GPBucket(EngineBucket):
    def __init__(self, gp, year):
        super().__init__(gp, year)
        
    
if __name__ == "__main__":
    from data_engine.cli import cli

    cli()