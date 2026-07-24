import modules.initial_analysis     as init
import modules.statistical_analysis as stat
import modules.subset_analysis      as sub
import modules.b_cell_calculation   as b_cell

HEADER_WIDTH = 50

def main():
    print(" Part 2: Initial Analysis - Data Overview ".center(HEADER_WIDTH, '='))
    samples_df = init.get_samples_df()
    print(samples_df, end="\n\n")

    print(" Part 3: Statistical Analysis ".center(HEADER_WIDTH, '='))
    stats_results = stat.statistical_analysis(samples_df)
    for population, p_val in stats_results.items():
        print(f"{population}: {p_val}")
    print()

    print(" Part 4 Data Subset Analysis ".center(HEADER_WIDTH, '='))
    subset_results = sub.subset_analysis()
    for query, table in subset_results.items():
        print(query, '\n', table, end='\n\n')
    
    print(" B-Cell Calculations ".center(HEADER_WIDTH, '='))
    avg_b_cells = b_cell.calc_avg_b_cells()
    print(f'Average number of b cells for the given condition: {avg_b_cells}', end='\n\n')

if __name__ == "__main__":
    main()
