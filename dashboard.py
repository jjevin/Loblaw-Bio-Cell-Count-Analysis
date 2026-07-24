import modules.initial_analysis     as init
import modules.statistical_analysis as stat
import modules.subset_analysis      as sub
import modules.b_cell_calculation   as b_cell

def main():
    samples_df = init.get_samples_df()
    stat.statistical_analysis(samples_df)
    sub.subset_analysis()
    b_cell.avg_b_cells()

if __name__ == "__main__":
    main()
