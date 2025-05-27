import streamlit as st

TROOP_TYPES = ['Mounted', 'Ranged', 'Ground', 'Siege']
TIERS = list(range(1, 17))

POWER_MULTIPLIER = {
    1: 1,
    2: 3,
    3: 9,
    4: 27,
    5: 81,
    6: 243,
    7: 729,
    8: 2187,
    9: 6561,
    10: 19683,
    11: 59049,
    12: 177147,
    13: 531441,
    14: 1594323,
    15: 4782969,
    16: 14348907,
}

T1_PERCENT_RANGES = {
    'Mounted': (1.0, 1.0),
    'Ranged': (0.10, 0.20),
    'Ground': (0.02, 0.05),
    'Siege': (0.01, 0.03),
}

SCALE_FACTOR = 0.75


def format_number(n):
    return f"{n:,}"

def parse_number(text):
    return int(str(text).replace(",", "").strip() or "0")

def main():
    st.title("Evony Defense Troop Layer Calculator")
    st.markdown("Enter **T11–T16 troop counts**, and this will balance **T1–T10** accordingly.")

    enable_t15 = st.checkbox("Enable T15")
    enable_t16 = st.checkbox("Enable T16")

    troop_data = {t: {} for t in TROOP_TYPES}

    with st.form("troop_input_form"):
        for t in TROOP_TYPES:
            st.subheader(f"{t} Troops")
            cols = st.columns(6)
            for i, tier in enumerate(range(11, 17)):
                if (tier == 15 and not enable_t15) or (tier == 16 and not enable_t16):
                    troop_data[t][tier] = 0
                    continue
                value = cols[i].text_input(f"T{tier} {t}", value="0", key=f"{t}_T{tier}")
                troop_data[t][tier] = parse_number(value)

        submitted = st.form_submit_button("Calculate Layers")

    if submitted:
        total_power_upper = 0
        for t in TROOP_TYPES:
            total_power_upper += sum(troop_data[t].get(tier, 0) * POWER_MULTIPLIER[tier] for tier in range(11, 17))

        power_sum = sum(POWER_MULTIPLIER[tier] * (SCALE_FACTOR ** (tier - 1)) for tier in range(1, 11))
        base_T1_mounted_count = int(total_power_upper / power_sum) if power_sum != 0 else 0

        T1_counts = {}
        for t in TROOP_TYPES:
            if t == 'Mounted':
                T1_counts[t] = base_T1_mounted_count
            else:
                avg_pct = sum(T1_PERCENT_RANGES[t]) / 2
                T1_counts[t] = int(base_T1_mounted_count * avg_pct)

        results = {t: {} for t in TROOP_TYPES}
        for t in TROOP_TYPES:
            for tier in range(1, 11):
                results[t][tier] = int(T1_counts[t] * (SCALE_FACTOR ** (tier - 1)))
            for tier in range(11, 17):
                results[t][tier] = troop_data[t][tier]

        st.markdown("### Balanced Troop Layers (T1–T16):")
        for t in TROOP_TYPES:
            st.markdown(f"**{t} Troops**")
            for tier in range(1, 17):
                st.write(f"T{tier}: {format_number(results[t][tier])}")
            st.markdown("---")

if __name__ == "__main__":
    main()