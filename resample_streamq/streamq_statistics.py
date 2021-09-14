import argparse
import xarray as xr
import matplotlib.pyplot as plt

vars_for_statistics = ["aprecip", "drainge", "soilh2o", "river_flow_rate_mod"]
vars_for_grouping = ["day", "month"]
internal_vars = ["time.dayofyear", "time.month"]
grouping_variables = dict(zip(vars_for_grouping, internal_vars))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_nc", type=str, help="Input file (TopNet streamq file)")
    parser.add_argument("-variable", type=str, choices=vars_for_statistics)
    parser.add_argument("-grouping", type=str, choices=vars_for_grouping)
    return parser.parse_args()


def main():
    args = parse_args()
    input_nc = args.input_nc
    grouping = args.grouping
    grouping_var = grouping_variables[grouping]
    variable = args.variable

    DS = xr.open_dataset(input_nc)
    DS_grouped = DS.get(variable).groupby(grouping_var)

    print(DS_grouped)
    mean_vals = DS_grouped.mean()
    ninety_five_quantile = DS_grouped.quantile(0.95)
    five_quantile = DS_grouped.quantile(0.05)

    mean_vals.plot()
    ninety_five_quantile[0].plot()
    five_quantile[0].plot()
    plt.show()

if __name__ == "__main__":
    main()
