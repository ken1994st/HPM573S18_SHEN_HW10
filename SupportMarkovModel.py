import InputData as Settings
import scr.FormatFunctions as F
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs
import scr.StatisticalClasses as Stat
import scr.EconEvalClasses as Econ


def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of time to stroke
    strokes_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_count_strokes().get_mean(),
        interval=simOutput.get_sumStat_count_strokes().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_cost().get_mean(),
        interval=simOutput.get_sumStat_discounted_cost().get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_utility().get_mean(),
        interval=simOutput.get_sumStat_discounted_utility().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean and {:.{prec}%} confidence interval of survival time:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean and {:.{prec}%} confidence interval of time to stroke:".format(1 - Settings.ALPHA, prec=0),
          strokes_mean_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")



def report_CEA_CBA(simOutputs_none, simOutputs_anticoag):
    """ performs cost-effectiveness analysis
    :param simOutputs_mono: output of a cohort simulated under mono therapy
    :param simOutputs_combo: output of a cohort simulated under combination therapy
    """

    # define two strategies
    none_therapy_strategy = Econ.Strategy(
        name='None Therapy',
        cost_obs=simOutputs_none.get_costs(),
        effect_obs=simOutputs_none.get_utilities()
    )
    anticoag_therapy_strategy = Econ.Strategy(
        name='Anticoag Therapy',
        cost_obs=simOutputs_anticoag.get_costs(),
        effect_obs=simOutputs_anticoag.get_utilities()
    )

    # CEA
    CEA = Econ.CEA(
        strategies=[none_therapy_strategy, anticoag_therapy_strategy],
        if_paired=False
        )

    # show the CE plane
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )

    # CBA

    NBA = Econ.CBA(
        strategies=[none_therapy_strategy, anticoag_therapy_strategy],
        if_paired=False
        )
    # show the net monetary benefit figure
    NBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval=Econ.Interval.CONFIDENCE,
        show_legend=True,
        figure_size=6
    )
