import cpast_scrapper.codechef as codechef
import cpast_scrapper.codeforces as codeforces


print(codechef.CodeChef().get_problems_by_code('NONNEGPROD').json())
print(codeforces.CodeForces().get_problems_by_code('1922', 'B').json())
