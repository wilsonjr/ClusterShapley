import shap 
import numpy as np
import matplotlib.pyplot as plt

def beeswarm(klass, shap_values, data, cluster_labels, feature_names, color_polyline='black',
                alpha_polyline=0.1, max_display=10, order_p=shap.Explanation.abs.mean(0),
             clustering=None, cluster_threshold=0.5, color=None,
             axis_color="#333333", alpha=1, show=True, log_scale=False,
             color_bar=True, plot_size="auto"):
    """Create a SHAP beeswarm plot, colored by feature values when they are provided.

    Attention: This is an adaptation from the original SHAP beeswarm plot. 
    <https://github.com/slundberg/shap/blob/master/shap/plots/_beeswarm.py>
    Here, we use polylines to investigate the SHAP values for the clustering assignments.

    Parameters
    ----------
    klass : int
        The clustering label
    shap_values : np.array
        This is a (k, n, m) matrix with SHAP values
    data : np.array
        The matrix used for explanation
    cluster_labels : np.array
        The respective clustering labels for "data"
    max_display : int
        How many top features to include in the plot (default is 20, or 7 for interaction plots)
    plot_size : "auto" (default), float, (float, float), or None
        What size to make the plot. By default the size is auto-scaled based on the number of
        features that are being displayed. Passing a single float will cause each row to be that 
        many inches high. Passing a pair of floats will scale the plot by that
        number of inches. If None is passed then the size of the current figure will be left
        unchanged.
    """
    values = shap_values[klass][cluster_labels == klass]
    feature_order = shap.plots._utils.convert_ordering(shap.Explanation.abs.mean(0), values)
    order = shap.plots._utils.convert_ordering(order_p, values)

    num_features = min(max_display, values.shape[1])
    values[:,feature_order[num_features-1]] = np.sum([values[:,feature_order[i]] for i in 
                                                      range(num_features-1, len(values[0]))], 0)

    values_ord = values[:, order]
    indices = np.arange(num_features).astype(int)[::-1]
    for i in range(values_ord.shape[0]):
        plt.plot(values_ord[i][:num_features], indices, color=color_polyline, alpha=alpha_polyline)

    c_exp = shap.Explanation(shap_values[klass], data=data, feature_names=feature_names)
    shap.plots.beeswarm(c_exp, max_display=num_features, order=order_p,
             clustering=clustering, cluster_threshold=cluster_threshold, color=color,
             axis_color=axis_color, alpha=alpha, log_scale=log_scale,
             color_bar=color_bar, plot_size=plot_size, show=False)

            