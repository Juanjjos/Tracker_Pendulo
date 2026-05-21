"""
Experimental configuration for 2^2 factorial design of pendulum damping study.

Design:
    Factor 1 (L): Hilo length = 30cm (Experiments 1,3) or 60cm (Experiments 2,4)
    Factor 2 (A): Area = sin_hojas/with leaves (1,2) or con_hojas/without leaves (3,4)
    
Response variable: β (damping coefficient in s⁻¹)
"""

# Physical constants
CONSTANTS = {
    'g': 9.7772,  # m/s² (Pereira value)
    'mass': 0.031797,  # kg (sphere mass)
    'sphere_radius': 0.0165,  # m
    'drag_coefficient_sphere': 0.47,
    'drag_coefficient_plate': 1.17,  # for leaves
}

# 2^2 Factorial Design Configuration
EXPERIMENTS = {
    1: {
        'experiment_id': 1,
        'name': 'Short, No Leaves',
        'hilo_length_cm': 30,
        'area_condition': 'sin_hojas',
        'description': 'Short string (30 cm) without attached leaves',
    },
    2: {
        'experiment_id': 2,
        'name': 'Long, No Leaves',
        'hilo_length_cm': 60,
        'area_condition': 'sin_hojas',
        'description': 'Long string (60 cm) without attached leaves',
    },
    3: {
        'experiment_id': 3,
        'name': 'Short, With Leaves',
        'hilo_length_cm': 30,
        'area_condition': 'con_hojas',
        'description': 'Short string (30 cm) with attached leaves',
    },
    4: {
        'experiment_id': 4,
        'name': 'Long, With Leaves',
        'hilo_length_cm': 60,
        'area_condition': 'con_hojas',
        'description': 'Long string (60 cm) with attached leaves',
    },
}

# Camera settings for each experiment
CAMERA_SETTINGS = {
    1: {'target_fps': 30, 'expected_period': 1.1},  # ~0.91 Hz
    2: {'target_fps': 30, 'expected_period': 1.56},  # ~0.64 Hz
    3: {'target_fps': 30, 'expected_period': 1.1},
    4: {'target_fps': 30, 'expected_period': 1.56},
}

# Signal processing parameters for each experiment
SIGNAL_PROCESSING = {
    'savgol_polyorder': 3,
    'find_peaks_min_distance': None,  # Will adapt to period
}


def get_experiment_config(experiment_id):
    """
    Get configuration for a specific experiment.
    
    Args:
        experiment_id (int): Experiment ID (1-4)
    
    Returns:
        dict: Configuration dictionary with all parameters
    """
    if experiment_id not in EXPERIMENTS:
        raise ValueError(f"Invalid experiment_id: {experiment_id}. Must be 1-4.")
    
    config = EXPERIMENTS[experiment_id].copy()
    config['constants'] = CONSTANTS.copy()
    config['camera'] = CAMERA_SETTINGS[experiment_id].copy()
    config['signal_processing'] = SIGNAL_PROCESSING.copy()
    
    return config


def get_all_experiments():
    """Get all experiment configurations."""
    return {eid: get_experiment_config(eid) for eid in range(1, 5)}


def print_experiment_summary():
    """Print summary of all experiments in the factorial design."""
    print("\n" + "="*60)
    print("2^2 FACTORIAL DESIGN - Pendulum Damping Study")
    print("="*60)
    
    for eid in range(1, 5):
        exp = EXPERIMENTS[eid]
        print(f"\nExperiment {eid}: {exp['name']}")
        print(f"  Description: {exp['description']}")
        print(f"  Hilo Length: {exp['hilo_length_cm']} cm")
        print(f"  Area Condition: {exp['area_condition']}")
        print(f"  Expected Period: {CAMERA_SETTINGS[eid]['expected_period']:.2f} s")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    print_experiment_summary()
    
    # Example: Get configuration for experiment 1
    config = get_experiment_config(1)
    print(f"Experiment 1 config: {config}")
