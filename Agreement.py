from typing import List
class Agreement:
    def __init__(self,company1,company2,pay : List,indemnization : float,duration_limit : int):
        self.part1 = (company1,pay)
        pay2 = [-pay[0]] + [p.amount for p in pay[1:]]
        self.part2 = (company2,pay2)
        self.indemnization = indemnization
        self.duration_limit = duration_limit
        self.duration = 0
    def compute_agreement(self):
        if self.part1[0].add_products(self.part1[1]):
            if not self.part2[0].add_products(self.part2[1]):
                self.part1[0].add_products([self.indemnization])
                self.part2[0].add_products([-self.indemnization])
        else:
            self.part1[0].add_products([-self.indemnization])
            self.part2[0].add_products([self.indemnization])
    def is_over(self):
        return self.duration >= self.duration_limit