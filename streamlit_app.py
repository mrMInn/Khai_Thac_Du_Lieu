
import graphviz
import streamlit as st
import pandas as pd
import itertools
import numpy as np
from itertools import combinations
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Cấu hình trang
st.set_page_config(
    page_title="Các Thuật Toán Khai Phá Dữ Liệu",
    layout="wide",
    initial_sidebar_state="expanded"
)


# TÙY CHỈNH GIAO DIỆN 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* MAIN CONTAINER */
    .main .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* SIDEBAR BUTTONS */
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        height: 70px !important;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    /* BUTTON HOVER EFFECT */
    section[data-testid="stSidebar"] .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover::before {
        left: 100%;
    }
    
    /* ACTIVE BUTTON */
    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* INACTIVE BUTTON */
    section[data-testid="stSidebar"] .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.7);
    }
    
    section[data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* RADIO BUTTONS - TAB STYLE */
    div.row-widget.stRadio > div {
        flex-direction: row;
        background: white;
        padding: 6px;
        border-radius: 16px;
        justify-content: center;
        flex-wrap: wrap;
        gap: 6px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    div.row-widget.stRadio > div label {
        background: transparent;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        cursor: pointer;
        color: #6c757d;
        border: 2px solid transparent;
    }
    
    div.row-widget.stRadio > div label:hover {
        background: rgba(102, 126, 234, 0.05);
        color: #667eea;
        transform: translateY(-1px);
    }
    
    div.row-widget.stRadio > div label:has(input:checked) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
        border-color: transparent;
    }
    
    /* HEADINGS */
    h1, h2, h3 {
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem !important;
    }
    
    h2 {
        color: #2d3748;
        font-size: 1.8rem !important;
        margin-top: 2.5rem !important;
    }
    
    h3 {
        color: #4a5568;
        font-size: 1.4rem !important;
    }
    
    /* EXPANDERS */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        font-weight: 600;
        padding: 1rem !important;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        border-color: #667eea;
        transform: translateX(4px);
    }
    
    /* METRICS */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #4a5568;
        font-size: 1rem;
    }
    
    /* DATAFRAMES */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* ALERT BOXES */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        padding: 1rem 1.5rem;
        font-weight: 500;
    }
    
    /* INFO BOX */
    .stAlert[data-baseweb="notification"][kind="info"] {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left-color: #2196f3;
    }
    
    /* SUCCESS BOX */
    .stAlert[data-baseweb="notification"][kind="success"] {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left-color: #4caf50;
    }
    
    /* WARNING BOX */
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left-color: #ff9800;
    }
    
    /* ERROR BOX */
    .stAlert[data-baseweb="notification"][kind="error"] {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left-color: #f44336;
    }
    
    /* PROGRESS BAR */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* BUTTONS IN MAIN AREA */
    .stButton button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        font-size: 1rem;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        padding: 8px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* CODE BLOCKS */
    .stCodeBlock {
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* DIVIDER */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* CUSTOM CARD STYLE */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
    }
    
    /* SIDEBAR TITLE */
    .sidebar-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* SELECTBOX */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
    }
    
    /* COLUMNS SPACING */
    [data-testid="column"] {
        padding: 0 0.75rem;
    }
    
    /* ANIMATION */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main .block-container > div {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)




# ==========================================
# 1. THUẬT TOÁN TẬP THÔ (ROUGH SET)
# ==========================================

def render_rough_set():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h3 style='color: #667eea; font-weight: 600;'>
                Tập thô
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Dữ liệu
    data = {
        "Tên người": ["Hoa","Lan","Xuân","Hạ","Thu","Đông","Mơ","Đào"],
        "Màu tóc": ["Đen","Đen","Râm","Đen","Bạc","Râm","Râm","Đen"],
        "Chiều cao": ["Tầm thước","Cao","Thấp","Thấp","Tầm thước","Cao","Tầm thước","Thấp"],
        "Cân nặng": ["Nhẹ","Vừa phải","Vừa phải","Vừa phải","Nặng","Nặng","Nặng","Nhẹ"],
        "Dùng thuốc": ["Không","Có","Có","Không","Không","Không","Không","Có"],
        "Kết quả": ["Bị rám","Không","Không","Bị rám","Bị rám","Không","Không","Không"]
    }
    
    df = pd.DataFrame(data).set_index("Tên người")
    condition_attrs = ["Màu tóc","Chiều cao","Cân nặng","Dùng thuốc"]
    decision_attr = "Kết quả"

    # Logic xử lý
    def ind_equivalence(df, attrs):
        groups = df.groupby(attrs)
        return [list(g.index) for _, g in groups]

    def lower_approx(eq_classes, X):
        lower = []
        for cls in eq_classes:
            if set(cls).issubset(X):
                lower.extend(cls)
        return sorted(lower)

    def upper_approx(eq_classes, X):
        upper = set()
        for cls in eq_classes:
            if set(cls).intersection(X):
                upper.update(cls)
        return sorted(list(upper))

    def positive_region(df, cond_attrs, dec_attr):
        eq_classes = ind_equivalence(df, cond_attrs)
        dec_values = df[dec_attr].unique()
        pos = set()
        for dv in dec_values:
            X_set = set(df[df[dec_attr] == dv].index)
            pos |= set(lower_approx(eq_classes, X_set))
        return sorted(list(pos))

    def dependency_degree(df, cond_attrs, dec_attr):
        pos = positive_region(df, cond_attrs, dec_attr)
        gamma = len(pos) / len(df)
        return gamma, pos

    def discernibility_matrix(df, attrs, dec):
        matrix = {}
        objs = df.index.tolist()
        for i in range(len(objs)):
            for j in range(i+1, len(objs)):
                oi, oj = objs[i], objs[j]
                if df.loc[oi, dec] == df.loc[oj, dec]:
                    matrix[(oi, oj)] = set()
                else:
                    diff = set()
                    for a in attrs:
                        if df.loc[oi, a] != df.loc[oj, a]:
                            diff.add(a)
                    matrix[(oi, oj)] = diff
        return matrix

    def build_clauses(M):
        clauses = []
        for pair, diff in M.items():
            if len(diff) > 0:
                clauses.append(diff)
        return clauses

    def find_reducts(clauses, attrs):
        candidates = []
        for r in range(1, len(attrs)+1):
            for comb in combinations(attrs, r):
                S = set(comb)
                ok = True
                for clause in clauses:
                    if S.isdisjoint(clause):
                        ok = False
                        break
                if ok:
                    candidates.append(S)
        
        reducts = []
        for R in candidates:
            if not any((other < R) for other in candidates if other != R):
                reducts.append(R)
        return reducts

    def gen_rules(df, reduct, dec):
        eq_classes = ind_equivalence(df, list(reduct))
        rules = []
        for cls in eq_classes:
            dec_vals = df.loc[cls, dec].unique()
            if len(dec_vals) == 1:
                rep = cls[0]
                premise = [(a, df.loc[rep,a]) for a in reduct]
                conclusion = dec_vals[0]
                rules.append((premise, conclusion, cls))
        return rules

    # Giao diện

    tabs = st.tabs([
        "Dữ liệu", 
        "Xấp xỉ & Phụ thuộc", 
        "Ma trận phân biệt & Reduct", 
        "Luật quyết định"
    ])

    with tabs[0]:
        st.info("Bảng dữ liệu ban đầu.")
        st.dataframe(df, use_container_width=True)

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 1. Quan hệ bất khả phân biệt IND(B)")
            demo_B = ["Màu tóc", "Cân nặng"]
            st.write(f"Xét tập thuộc tính **B = {demo_B}**:")
            ind_B = ind_equivalence(df, demo_B)
            formatted_ind = [str(cls) for cls in ind_B]
            st.code("\n".join(formatted_ind), language="text")

        with col2:
            st.markdown("##### 2. Xấp xỉ Dưới/Trên")
            target_val = "Bị rám"
            X_set = set(df[df["Kết quả"] == target_val].index)
            approx_attrs = ["Màu tóc", "Chiều cao"]
            eq_approx = ind_equivalence(df, approx_attrs)
            lower = lower_approx(eq_approx, X_set)
            upper = upper_approx(eq_approx, X_set)
            
            st.write(f"Xét tập **X = '{target_val}'** và tập thuộc tính **{approx_attrs}**:")
            st.success(f"**Lower Approx:** {lower}")
            st.warning(f"**Upper Approx:** {upper}")

        st.divider()
        st.markdown("##### 3. Độ phụ thuộc dữ liệu Gamma(B,D)")
        gamma, pos = dependency_degree(df, condition_attrs, decision_attr)
        st.write(f"Vùng dương POS = {pos}")
        st.metric("Hệ số phụ thuộc Gamma", f"{gamma:.4f}")

    with tabs[2]:
        st.markdown("##### 4. Ma trận phân biệt")
        M = discernibility_matrix(df, condition_attrs, decision_attr)
        objs = df.index.tolist()
        matrix_display = []
        for i, oi in enumerate(objs):
            row_data = {}
            for j, oj in enumerate(objs):
                if j > i: val = ""
                elif i == j: val = "—"
                else:
                    diff = M.get((oi, oj)) or M.get((oj, oi))
                    if diff is None or len(diff) == 0: val = "Empty"
                    else: val = ", ".join(diff)
                row_data[oj] = val
            matrix_display.append(row_data)
        
        df_matrix = pd.DataFrame(matrix_display, index=objs)
        st.dataframe(df_matrix, use_container_width=True)

        st.markdown("##### 5. Rút gọn thuộc tính (Tìm các Reducts)")
        clauses = build_clauses(M)
        reducts = find_reducts(clauses, condition_attrs)
        if reducts:
            for idx, r in enumerate(reducts):
                st.success(f"**Reduct {idx+1}:** {list(r)}")
        else:
            st.warning("Không tìm thấy Reduct nào.")

    with tabs[3]:
     st.markdown("##### 6. Liệt kê luật quyết định có độ chính xác 100%")
     if not reducts:
        st.write("Cần tìm Reduct trước khi sinh luật.")
     else:
        for i, r in enumerate(reducts):
            with st.expander(f"Luật từ Reduct {i+1}: {list(r)}", expanded=True):
                rules = gen_rules(df, r, decision_attr)
                
                if not rules:
                    st.write("Không sinh được luật nào 100%.")
                else:
                    # 1. Hiển thị tổng số luật
                    st.markdown(f"**Tổng số luật sinh ra: {len(rules)}**")
                    
                    # 2. Vòng lặp với enumerate để lấy số thứ tự (idx bắt đầu từ 1)
                    for idx, (prem, concl, cls) in enumerate(rules, 1):
                        prem_str = " AND ".join([f"**{a}**='{v}'" for a, v in prem])
                        
                        # Thay dấu gạch đầu dòng (-) bằng Luật {idx}
                        st.markdown(f"""
                        **Luật {idx}:** NẾU {prem_str}
                          &nbsp;&nbsp;THÌ **{decision_attr}** = <span style='color:red'>{concl}</span> 
                          &nbsp;*(Áp dụng cho: {cls})*
                        """, unsafe_allow_html=True)

# ==========================================
# 2. THUẬT TOÁN TẬP PHỔ BIẾN (APRIORI)
# ==========================================

def render_frequent_itemset():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h3 style='color: #667eea; font-weight: 600; margin-bottom: 0.5rem;'>
                Chọn bước thực hiện
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    sub_menu = st.radio(
        "",
        [
            "Dữ liệu ban đầu",
            "Tập phổ biến",
            "Tập phổ biến tối đại",
            "Luật kết hợp"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dữ liệu
    giaodich = [
        {'i1','i2','i3'}, {'i2','i3','i4'}, {'i2','i3','i4'}, {'i1','i2','i3'}, {'i3','i4'}
    ]
    
    def apriori(giaodich, min_support=0.4, min_confidence=0.7):
        giao_dich = list(map(frozenset, giaodich))
        tong = len(giao_dich)
        min_sup_count = max(1, int(min_support * tong))

        dem = defaultdict(int)
        for gd in giao_dich:
            for item in gd:
                dem[frozenset([item])] += 1

        L = {i for i, c in dem.items() if c >= min_sup_count}
        freq = {tuple(i): dem[i] for i in L}

        k = 1
        while L:
            k += 1
            ungvien = set()
            L_list = list(L)
            for i in range(len(L_list)):
                for j in range(i+1, len(L_list)):
                    hop = L_list[i] | L_list[j]
                    if len(hop) == k:
                        ungvien.add(hop)
            valid = {c for c in ungvien if all(frozenset(s) in L for s in combinations(c, k-1))}
            demUV = defaultdict(int)
            for gd in giao_dich:
                for c in valid:
                    if c.issubset(gd):
                        demUV[c] += 1
            L = {c for c in demUV if demUV[c] >= min_sup_count}
            freq.update({tuple(sorted(c)): demUV[c] for c in L})

        df_freq = pd.DataFrame([(items, cnt, cnt/tong) for items,cnt in freq.items()],
                               columns=["Tập mục","Số lần","Support"])

        rules = []
        for items,cnt in freq.items():
            items=set(items)
            if len(items)>1:
                for r in range(1,len(items)):
                    for A in combinations(items,r):
                        A=set(A); B=items-A
                        sup_AB=cnt/tong
                        sup_A=freq.get(tuple(sorted(A)),0)/tong
                        sup_B=freq.get(tuple(sorted(B)),0)/tong
                        conf=sup_AB/sup_A if sup_A else 0
                        lift=conf/sup_B if sup_B else 0
                        if conf>=min_confidence:
                            rules.append([tuple(A),tuple(B),sup_AB,conf,lift])

        df_rules=pd.DataFrame(rules,columns=["A=>","B=>","Support","Confidence","Lift"])
        return df_freq, df_rules
    
    def find_maximal_frequent_itemsets(freq_df):
        itemsets = [set(items) for items in freq_df["Tập mục"]]
        maximal_sets = []
        for i in range(len(itemsets)):
            is_maximal = True
            for j in range(len(itemsets)):
                if i != j and itemsets[i].issubset(itemsets[j]):
                    if len(itemsets[i]) < len(itemsets[j]):
                        is_maximal = False
                        break
            if is_maximal:
                maximal_sets.append(itemsets[i])
        return maximal_sets
    
    freq, rules = apriori(giaodich, 0.4, 0.7)
    maximal = find_maximal_frequent_itemsets(freq)
    
    if sub_menu == "Dữ liệu ban đầu":
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
                <h2 style='color: white; margin: 0; font-size: 2rem;'>Dữ liệu giao dịch</h2>
                <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem; margin-bottom: 0;'>
                    Dữ liệu gồm <strong>5 giao dịch</strong> với các sản phẩm i1, i2, i3, i4.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        data_display = []
        for idx, items in enumerate(giaodich, 1):
            row = {'Giao dịch': f'o{idx}'}
            for i in range(1, 5):
                row[f'i{i}'] = 'X' if f'i{i}' in items else ''
            data_display.append(row)
        
        df_display = pd.DataFrame(data_display)
        st.dataframe(df_display, use_container_width=True, height=250)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"Tổng giao dịch: 5")
        with col2:
            st.info(f"Min Support: 40%")
        with col3:
            st.info(f"Min Confidence: 70%")
        
        
    
    elif sub_menu == "Tập phổ biến":
        st.markdown("### Tập phổ biến")
        st.info(f"**Tổng số tập phổ biến tìm được**: {len(freq)}")
        
        freq_display = freq.copy()
        freq_display['Tập mục'] = freq_display['Tập mục'].apply(lambda x: '{' + ', '.join(sorted(x)) + '}')
        freq_display['Support'] = freq_display['Support'].apply(lambda x: f'{x:.2%}')
        
        st.dataframe(freq_display, use_container_width=True, height=400)
        
        st.subheader("Phân loại theo kích thước tập")
        sizes = freq.groupby(freq['Tập mục'].apply(len)).size()
        for size, count in sizes.items():
            with st.expander(f"**Tập {size}-mục** ({count} tập)", expanded=True):
                subset = freq[freq['Tập mục'].apply(len) == size].copy()
                subset['Tập mục'] = subset['Tập mục'].apply(lambda x: '{' + ', '.join(sorted(x)) + '}')
                subset['Support'] = subset['Support'].apply(lambda x: f'{x:.2%}')
                st.dataframe(subset, use_container_width=True)
    
    elif sub_menu == "Tập phổ biến tối đại":
        st.markdown("### Tập phổ biến tối đại")
        st.info(f"**Số lượng tập phổ biến tối đại**: {len(maximal)}")
        
        for idx, m in enumerate(maximal, 1):
            items_sorted = sorted(m)
            items_str = ', '.join(items_sorted)
            st.success(f"**Tập {idx}:** {{{items_str}}}")
    
    elif sub_menu == "Luật kết hợp":
        st.markdown("### Luật kết hợp")
        if len(rules) > 0:
            st.info(f"**Tổng số luật kết hợp**: {len(rules)}")
            
            rules_display = rules.copy()
            rules_display['A=>'] = rules_display['A=>'].apply(lambda x: '{' + ', '.join(sorted(x)) + '}')
            rules_display['B=>'] = rules_display['B=>'].apply(lambda x: '{' + ', '.join(sorted(x)) + '}')
            rules_display['Support'] = rules_display['Support'].apply(lambda x: f'{x:.2%}')
            rules_display['Confidence'] = rules_display['Confidence'].apply(lambda x: f'{x:.2%}')
            rules_display['Lift'] = rules_display['Lift'].apply(lambda x: f'{x:.3f}')
            
            st.dataframe(rules_display, use_container_width=True, height=400)
            
            st.subheader("Chi tiết các luật")
            for idx, row in rules.iterrows():
                A = sorted(row['A=>'])
                B = sorted(row['B=>'])
                A_str = '{' + ', '.join(A) + '}'
                B_str = '{' + ', '.join(B) + '}'
                st.write(f"**Luật {idx+1}:** {A_str} => {B_str} | Support: {row['Support']:.2%} | Confidence: {row['Confidence']:.2%} | Lift: {row['Lift']:.3f}")
        else:
            st.warning("Không tìm thấy luật kết hợp nào thỏa mãn điều kiện!")

# ==========================================
# 3. THUẬT TOÁN CÂY QUYẾT ĐỊNH (DECISION TREE)
# ==========================================

def render_decision_tree():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h3 style='color: #667eea; font-weight: 600; margin-bottom: 0.5rem;'>
                Chọn phương pháp xây dựng cây quyết định
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    sub_menu = st.radio(
        "",
        [
            "Information Gain",
            "Gini Index"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    if sub_menu == "Information Gain":
        render_information_gain_tree()
    elif sub_menu == "Gini Index":
        render_gini_index_tree()


def render_information_gain_tree():
    st.markdown("### Information Gain")
    
    # 1. Dữ liệu mẫu 
    raw_data = {
        'Day': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain', 'Sunny', 'Overcast', 'Overcast', 'Rain'],
        'Temp': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
        'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
        'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Strong', 'Weak', 'Strong'],
        'Play': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
    }
    weather_df = pd.DataFrame(raw_data)
    st.info("Bảng dữ liệu ban đầu.")
    st.dataframe(weather_df, use_container_width=True, height=300)
    
    feature_attributes = ['Outlook', 'Temp', 'Humidity', 'Wind']
    target_attribute = 'Play'
    
    # Hàm tính Entropy
    def calculate_entropy(series):
        counts = series.value_counts()
        probabilities = counts / len(series)
        entropy = 0
        for p in probabilities:
            if p > 0:
                entropy += -p * np.log2(p)
        return entropy
    
    # Tính Entropy hệ thống (S)
    total_entropy = calculate_entropy(weather_df[target_attribute])
    st.info(f"**Entropy hệ thống (Play)**: {total_entropy:.4f}")
    
    # 2. Tính toán chi tiết Information Gain 
    ig_summary_results = []
    
    st.subheader("Chi tiết tính toán Information Gain cho từng thuộc tính")
    
    for feature in feature_attributes:
        # Lấy các giá trị duy nhất của thuộc tính (ví dụ: Sunny, Overcast, Rain)
        values = weather_df[feature].unique()
        weighted_average_entropy = 0
        details = []
        
        # Duyệt qua từng giá trị con để tính Entropy thành phần
        for value in values:
            subset = weather_df[weather_df[feature] == value]
            subset_entropy = calculate_entropy(subset[target_attribute])
            weight = len(subset) / len(weather_df)
            weighted_average_entropy += weight * subset_entropy
            
            # Lưu chi tiết để hiển thị
            details.append({
                'Giá trị': value,
                'Số lượng': len(subset),
                'Entropy con': f'{subset_entropy:.4f}',
                'Trọng số': f'{weight:.4f}'
            })
            
        # Tính IG
        information_gain = total_entropy - weighted_average_entropy
        ig_summary_results.append({'Thuộc tính': feature, 'Information Gain': f'{information_gain:.4f}'})
        
        # Hiển thị Expanders giống bên Gini
        with st.expander(f"**{feature}** - Information Gain = {information_gain:.4f}"):
            st.markdown(f"Weighted Entropy: `{weighted_average_entropy:.4f}`")
            st.markdown(f"IG = {total_entropy:.4f} - {weighted_average_entropy:.4f} = **{information_gain:.4f}**")
            st.dataframe(pd.DataFrame(details), use_container_width=True)

    # Hiển thị bảng tổng hợp IG
    st.subheader("Bảng tổng hợp Information Gain")
    st.dataframe(pd.DataFrame(ig_summary_results), use_container_width=True)
    
    # 3. Class Node và Build Tree (Giữ nguyên logic cũ nhưng cần hàm calculate_information_gain tách riêng để chạy đệ quy)
    # LƯU Ý: Để hàm đệ quy build_tree hoạt động độc lập, ta cần khai báo lại hàm tính IG đơn giản
    def get_ig_simple(df, feat, target):
        e_total = calculate_entropy(df[target])
        e_weighted = 0
        for v in df[feat].unique():
            sub = df[df[feat] == v]
            e_weighted += (len(sub)/len(df)) * calculate_entropy(sub[target])
        return e_total - e_weighted

    class NodeIG:
        def __init__(self, attribute=None, value=None, result=None):
            self.attribute = attribute
            self.value = value
            self.result = result
            self.children = {}
        def add_child(self, value, node):
            self.children[value] = node
            
    def build_id3_tree_ig(df, available_attributes, target_attribute, parent_node=None, branch_value=None):
        # Nút lá: Chỉ còn 1 kết quả duy nhất
        if df[target_attribute].nunique() == 1:
            result = df[target_attribute].iloc[0]
            node = NodeIG(result=result)
            if parent_node is not None:
                parent_node.add_child(branch_value, node)
            return node
        
        # Nút lá: Hết thuộc tính để chia -> lấy theo số đông
        if not available_attributes or df.empty:
            if df.empty:
                # Trường hợp hiếm: tập dữ liệu rỗng
                return NodeIG(result="Unknown") 
            majority_class = df[target_attribute].mode()[0]
            node = NodeIG(result=majority_class)
            if parent_node is not None:
                parent_node.add_child(branch_value, node)
            return node
            
        # Chọn thuộc tính tốt nhất
        information_gains = {}
        for attr in available_attributes:
            ig = get_ig_simple(df, attr, target_attribute)
            information_gains[attr] = ig
            
        best_attribute = max(information_gains, key=information_gains.get)
        current_node = NodeIG(attribute=best_attribute)
        
        if parent_node is not None:
            parent_node.add_child(branch_value, current_node)
            
        new_available_attributes = [attr for attr in available_attributes if attr != best_attribute]
        
        for value in df[best_attribute].unique():
            subset = df[df[best_attribute] == value].reset_index(drop=True)
            build_id3_tree_ig(subset, new_available_attributes, target_attribute, parent_node=current_node, branch_value=value)
            
        return current_node

    id3_tree_ig = build_id3_tree_ig(weather_df, feature_attributes, target_attribute)
    
    # 4. Trực quan hóa cây
    st.subheader("Trực quan hóa cây quyết định (Information Gain)")
    
    def export_graphviz(node, dot=None, parent_id=None, edge_label=None):
        if dot is None:
            dot = graphviz.Digraph(comment='Decision Tree')
            dot.attr(rankdir='TB') 
            dot.attr('node', shape='ellipse', style='filled', color='lightblue', fontname="Sans-Serif")
        
        node_id = str(id(node))
        
        if node.result is not None:
            label = str(node.result)
            fillcolor = '#90EE90' if label == 'Yes' else '#FFB6C1' 
            dot.node(node_id, label, shape='box', style='filled,rounded', fillcolor=fillcolor)
        else:
            label = str(node.attribute)
            dot.node(node_id, label, shape='ellipse', style='filled', fillcolor='#E0F7FA')
        
        if parent_id is not None:
            dot.edge(parent_id, node_id, label=str(edge_label), fontsize='10', fontcolor='#555555')
            
        if node.children:
            for value, child in node.children.items():
                export_graphviz(child, dot, node_id, value)
                
        return dot

    try:
        dot = export_graphviz(id3_tree_ig)
        col_left, col_mid, col_right = st.columns([1, 5, 1])
        with col_mid:
            st.graphviz_chart(dot)
    except Exception as e:
        st.error(f"Lỗi khi vẽ cây: {e}")

#5. Hàm đệ quy để trích xuất luật từ cây
    def generate_rules(node, path=""):
        rules = []
        result = getattr(node, 'result', None) or getattr(node, 'results', None)
        
        if result is not None:
            # Làm sạch chuỗi đường dẫn (bỏ chữ " AND " thừa ở đầu)
            clean_path = path[5:] if path.startswith(" AND ") else path
            return [f"IF {clean_path} THEN Play = {result}"]
        
        # Nếu là node quyết định
        if getattr(node, 'children', None):
            # Gini dùng list children, IG dùng dict children
            children_iter = node.children.items() if isinstance(node.children, dict) else [(child.value, child) for child in node.children]
            
            for value, child_node in children_iter:
                new_condition = f" AND {node.attribute} = {value}"
                rules.extend(generate_rules(child_node, path + new_condition))
        
        return rules
    
    # --- PHẦN HIỂN THỊ LUẬT (Đã thêm đếm số lượng và thứ tự) ---
    #st.divider()
    st.subheader("Luật quyết định sinh ra từ cây (Information Gain)")
    
    rules_list = generate_rules(id3_tree_ig) 
    
    if len(rules_list) > 0:
        # 1. Hiển thị tổng số luật
        st.success(f"**Tổng cộng có: {len(rules_list)} luật**")
        
        # 2. Hiển thị từng luật với số thứ tự
        for i, rule in enumerate(rules_list, 1):
            st.markdown(f"**Luật {i}:**")
            st.code(rule, language='sql')
    else:
        st.warning("Không tìm thấy luật nào.")



def render_gini_index_tree():
    st.markdown("### Gini Index")
    data = {
        'Day': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Rainy', 'Sunny', 'Overcast', 'Overcast', 'Rainy'],
        'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
        'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
        'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
        'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
    }
    df = pd.DataFrame(data).drop(columns=['Day'])
    st.info("Bảng dữ liệu ban đầu.")
    st.dataframe(df, use_container_width=True, height=300)
    
    target = 'Play'
    attributes = ['Outlook', 'Temperature', 'Humidity', 'Wind']
    
    def calculate_gini(labels):
        total = len(labels)
        if total == 0: return 0
        counts = labels.value_counts()
        impurity = 1
        for count in counts:
            prob = count / total
            impurity -= prob ** 2
        return impurity
    
    def calculate_attribute_gini(df, attribute, target_name):
        values = df[attribute].unique()
        total_gini = 0
        total_rows = len(df)
        details = []
        for value in values:
            subset = df[df[attribute] == value]
            gini_subset = calculate_gini(subset[target_name])
            weight = len(subset) / total_rows
            total_gini += weight * gini_subset
            counts = subset[target_name].value_counts().to_dict()
            details.append({'Giá trị': value, 'Gini': f'{gini_subset:.4f}'})
        return total_gini, details

    initial_gini = calculate_gini(df[target])
    st.info(f"**Gini Index ban đầu**: {initial_gini:.4f}")

    st.subheader("Chi tiết tính toán Gini Index cho từng thuộc tính")
    
    for attr in attributes:
        gini, details = calculate_attribute_gini(df, attr, target)
        with st.expander(f"**{attr}** - Gini = {gini:.4f}"):
            st.dataframe(pd.DataFrame(details))

    # Class Node và Build Tree
    class NodeGini:
        def __init__(self, attribute=None, value=None, results=None, children=None):
            self.attribute = attribute
            self.value = value
            self.results = results
            self.children = children if children is not None else []
            
    def build_tree_gini(df, target_name, available_attributes):
        if len(df[target_name].unique()) == 1:
            return NodeGini(results=df[target_name].iloc[0])
        if not available_attributes:
            most_common = df[target_name].mode()[0]
            return NodeGini(results=most_common)
        best_gini = float('inf')
        best_attr = None
        for attr in available_attributes:
            gini, _ = calculate_attribute_gini(df, attr, target_name)
            if gini < best_gini:
                best_gini = gini
                best_attr = attr
        node = NodeGini(attribute=best_attr)
        unique_values = df[best_attr].unique()
        new_attributes = [x for x in available_attributes if x != best_attr]
        for value in unique_values:
            sub_df = df[df[best_attr] == value]
            child_node = build_tree_gini(sub_df, target_name, new_attributes)
            child_node.value = value
            node.children.append(child_node)
        return node

    decision_tree = build_tree_gini(df, target, attributes)
    
    # Vẽ cây quyết định Gini Index
    st.subheader("Trực quan hóa cây quyết định (Gini Index)")

    def export_graphviz_gini(node, dot=None, parent_id=None, edge_label=None):
     if dot is None:
        # Tạo đối tượng đồ thị
        dot = graphviz.Digraph(comment='Decision Tree')
        dot.attr(rankdir='TB') # Vẽ từ trên xuống
        dot.attr('node', shape='ellipse', style='filled', color='lightblue', fontname="Sans-Serif")
    
    # Tạo ID duy nhất cho node
     node_id = str(id(node))
     if node.results is not None:
        # ĐÂY LÀ NODE LÁ
            label = str(node.results)
        # Màu sắc
            fillcolor = '#90EE90' if label == 'Yes' else '#FFB6C1' 
            dot.node(node_id, label, shape='box', style='filled,rounded', fillcolor=fillcolor)
     else:
        # ĐÂY LÀ NODE QUYẾT ĐỊNH
         label = str(node.attribute)
         dot.node(node_id, label, shape='ellipse', style='filled', fillcolor='#E0F7FA')
    
    # Vẽ cạnh nối từ cha đến con
     if parent_id is not None:
      dot.edge(parent_id, node_id, label=str(edge_label), fontsize='10', fontcolor='#555555')
        
     if getattr(node, 'children', None):
        for child in node.children:
         export_graphviz_gini(child, dot, node_id, child.value)
        return dot
# Gọi hàm vẽ và hiển thị
    try:
        dot = export_graphviz_gini(decision_tree)
    
        col_left, col_mid, col_right = st.columns([1, 2, 1])
        with col_mid:
            st.graphviz_chart(dot)
    except Exception as e:
     st.error(f"Lỗi khi vẽ cây: {e}")

#5. Hàm đệ quy để trích xuất luật từ cây
    def generate_rules(node, path=""):
        rules = []
        result = getattr(node, 'result', None) or getattr(node, 'results', None)
        
        if result is not None:
            # Làm sạch chuỗi đường dẫn (bỏ chữ " AND " thừa ở đầu)
            clean_path = path[5:] if path.startswith(" AND ") else path
            return [f"IF {clean_path} THEN Play = {result}"]
        
        # Nếu là node quyết định
        if getattr(node, 'children', None):
            # Gini dùng list children, IG dùng dict children
            children_iter = node.children.items() if isinstance(node.children, dict) else [(child.value, child) for child in node.children]
            
            for value, child_node in children_iter:
                new_condition = f" AND {node.attribute} = {value}"
                rules.extend(generate_rules(child_node, path + new_condition))
        
        return rules
    
    # --- PHẦN HIỂN THỊ LUẬT (Đã thêm đếm số lượng và thứ tự) ---
    #st.divider()
    st.subheader("Luật quyết định sinh ra từ cây (Gini Index)")
    
    rules_list = generate_rules(decision_tree) 
    
    if len(rules_list) > 0:
        # 1. Hiển thị tổng số luật
        st.success(f"**Tổng cộng có: {len(rules_list)} luật**")
        
        # 2. Hiển thị từng luật với số thứ tự
        for i, rule in enumerate(rules_list, 1):
            st.markdown(f"**Luật {i}:**")
            st.code(rule, language='sql')
    else:
        st.warning("Không tìm thấy luật nào.")
    
# ==========================================
# 4. THUẬT TOÁN NAIVE BAYES
# ==========================================

def render_naive_bayes():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h3 style='color: #667eea; font-weight: 600; margin-bottom: 0.5rem;'>
                Phân lớp bằng thuật toán Naive Bayes
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    sub_menu = st.radio(
        "",
        ["Dữ liệu & Train", "Dự đoán"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("---")

    data = {
        "Outlook":    ["Sunny","Sunny","Overcast","Rainy","Rainy","Rainy","Overcast","Sunny","Sunny","Rainy","Sunny","Overcast","Overcast","Rainy"],
        "Temperature":["Hot","Hot","Hot","Mild","Cool","Cool","Cool","Mild","Cool","Mild","Mild","Mild","Hot","Mild"],
        "Humidity":   ["High","High","High","High","Normal","Normal","Normal","High","Normal","Normal","Normal","High","Normal","High"],
        "Wind":       ["Weak","Strong","Weak","Weak","Weak","Strong","Strong","Weak","Weak","Weak","Strong","Strong","Weak","Strong"],
        "Play":       ["No","No","Yes","Yes","Yes","No","Yes","No","Yes","Yes","Yes","Yes","Yes","No"]
    }
    df = pd.DataFrame(data)

    def train_naive_bayes(df, class_col):
        model = {}
        classes = df[class_col].unique()
        m = len(classes)
        total = len(df)
        model["priors"] = {}
        for c in classes:
            count_c = len(df[df[class_col] == c])
            model["priors"][c] = (count_c + 1) / (total + m)
        model["likelihoods"] = defaultdict(dict)
        for col in df.columns:
            if col == class_col: continue
            values = df[col].unique()
            r = len(values)
            for c in classes:
                subset = df[df[class_col] == c]
                model["likelihoods"][col][c] = {}
                for v in values:
                    count = len(subset[subset[col] == v])
                    model["likelihoods"][col][c][v] = (count + 1) / (len(subset) + r)
        return model

    model = train_naive_bayes(df, "Play")

    if sub_menu == "Dữ liệu & Train":
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Dữ liệu huấn luyện")
            st.dataframe(df, height=300)
        with c2:
            st.subheader("Tham số mô hình")
            st.write("**1. P(C):**")
            priors_df = pd.DataFrame(list(model['priors'].items()), columns=['Class', 'P(C)'])
            st.dataframe(priors_df.style.format({"P(C)": "{:.3f}"}), use_container_width=True)
            st.write("**2. P(X|C):**")
            likelihood_data = []
            for feat in ['Outlook', 'Humidity']: 
                for c in model['priors']:
                    for v in model['likelihoods'][feat][c]:
                        likelihood_data.append({'Feature': feat, 'Val': v, 'Class': c, 'Prob': model['likelihoods'][feat][c][v]})
            l_df = pd.DataFrame(likelihood_data).head(5)
            #st.table(l_df.style.format({"Prob": "{:.3f}"}))
            st.dataframe(l_df.style.format({"Prob": "{:.3f}"}), use_container_width=True)

    elif sub_menu == "Dự đoán":
        st.subheader("Chọn trường hợp kiểm thử")
        test_mode = st.radio(
            "Chọn chế độ nhập:",
            ["Test Case X1", "Test Case X2", "Tự nhập tùy ý"],
            horizontal=True
        )
        input_X = {}
        if test_mode == "Test Case X1":
            st.info("X1 = {Outlook: Sunny, Humidity: High}")
            input_X = {"Outlook": "Sunny", "Humidity": "High"}
        elif test_mode == "Test Case X2":
            st.info("X2 = {Outlook: Sunny, Humidity: Normal}")
            input_X = {"Outlook": "Sunny", "Humidity": "Normal"}
        else:
            c1, c2, c3, c4 = st.columns(4)
            with c1: input_X["Outlook"] = st.selectbox("Outlook", df['Outlook'].unique())
            with c2: input_X["Humidity"] = st.selectbox("Humidity", df['Humidity'].unique())
            with c3: input_X["Temperature"] = st.selectbox("Temperature", df['Temperature'].unique())
            with c4: input_X["Wind"] = st.selectbox("Wind", df['Wind'].unique())

        if st.button("Chạy Dự Đoán", type="primary"):
            st.markdown("### TÍNH TOÁN CHI TIẾT")
            results = {}
            cols = st.columns(len(model["priors"]))
            for idx, c in enumerate(model["priors"]):
                with cols[idx]:
                    if c == "Yes":
                        st.success(f"LỚP: {c}") 
                    else:
                        st.error(f"LỚP: {c}")
                    prior = model['priors'][c]
                    st.write(f"**P({c})** = `{prior:.3f}`")
                    prob = prior
                    explanation = [f"{prior:.3f}"]
                    for attr, value in input_X.items():
                        if attr in model["likelihoods"]:
                            p = model["likelihoods"][attr][c].get(value, 0)
                            st.write(f"- P({value} | {c}) = `{p:.3f}`")
                            prob *= p
                            explanation.append(f"{p:.3f}")
                    results[c] = prob
                    st.markdown("---")
                    st.write(f"**P(X|{c})** = {' x '.join(explanation)}")
                    st.markdown(f"**= {prob:.3f}**") 

            best = max(results, key=results.get)
            st.markdown("---")
            if best == "Yes":
                st.success(f"### KẾT QUẢ DỰ ĐOÁN: **{best} (Đi chơi)**")
            else:
                st.error(f"### KẾT QUẢ DỰ ĐOÁN: **{best} (Không đi chơi)**")

# ==========================================
# 5. THUẬT TOÁN GOM CỤM (CLUSTERING)
# ==========================================

def render_clustering():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <h3 style='color: #667eea; font-weight: 600; margin-bottom: 0.5rem;'>
                Thuật toán gom cụm K-Means
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    sub_menu = st.radio(
        "",
        [
            "Dữ liệu ban đầu",
            "Quá trình Gom cụm",
            "Biểu đồ Kết quả"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    X = np.array([
        [0.7, 0.45], [2.8, 1.0], [2.6, 1.0], [1.0, 0.8], [2.5, 1.2],
        [1.3, 1.4], [0.4, 0.7], [1.7, 1.8], [2.0, 2.0]
    ])
    df = pd.DataFrame(X, columns=["Chiều 1", "Chiều 2"])
    df.index = [f"x{i+1}" for i in range(len(X))]

    def euclid(a, b):
        return np.sqrt(np.sum((a - b) ** 2))

    k = 3
    initial_centroids = np.array([X[0], X[1], X[2]]) 

    if sub_menu == "Dữ liệu ban đầu":
        st.markdown("### Dữ liệu đầu vào")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(df, use_container_width=True, height=400)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter(X[:, 0], X[:, 1], c='gray', s=100, alpha=0.6)
            for i, txt in enumerate(df.index):
                ax.annotate(txt, (X[i, 0]+0.05, X[i, 1]+0.05))
            ax.set_title("Phân bố dữ liệu ban đầu")
            ax.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig)

    elif sub_menu == "Quá trình Gom cụm":
        st.markdown("### Chi tiết thuật toán K-Means")
        centroids = initial_centroids.copy()
        labels_old = None
        iteration = 1
        st.info(f"**Khởi tạo (k={k}):** Trọng tâm ban đầu: x1, x2, x3")
        
        while True:
            with st.expander(f"LẦN LẶP {iteration}", expanded=(iteration==1)):
                distances_list = []
                for i, x in enumerate(X):
                    d = [euclid(x, c) for c in centroids]
                    distances_list.append(d)
                distances = np.array(distances_list)
                dist_df = pd.DataFrame(distances, columns=[f"Đến C{j+1}" for j in range(k)], index=df.index)
                st.write("**1. Bảng khoảng cách:**")
                st.dataframe(dist_df, use_container_width=True)

                labels = np.argmin(distances, axis=1)
                cluster_dict = defaultdict(list)
                for idx, lab in enumerate(labels):
                    cluster_dict[lab].append(f"x{idx+1}")
                st.write("**2. Kết quả gán cụm:**")
                cols = st.columns(k)
                for i in range(k):
                    with cols[i]:
                        members = ", ".join(cluster_dict[i])
                        st.success(f"**Cụm {i+1}:** {members}")

                is_converged = False
                if labels_old is not None and np.all(labels == labels_old):
                    is_converged = True
                labels_old = labels.copy()

                new_centroids = []
                st.write("**3. Cập nhật trọng tâm mới:**")
                c_cols = st.columns(k)
                for i in range(k):
                    cluster_points = X[labels == i]
                    if len(cluster_points) > 0:
                        new_c = np.mean(cluster_points, axis=0)
                    else:
                        new_c = centroids[i]
                    new_centroids.append(new_c)
                    with c_cols[i]:
                        st.info(f"**v{i+1}** = [{new_c[0]:.3f}, {new_c[1]:.3f}]")
                centroids = np.array(new_centroids)
            
            if is_converged:
                st.success(f"### Thuật toán HỘI TỤ tại lần lặp thứ {iteration}!")
                break
            iteration += 1

    elif sub_menu == "Biểu đồ Kết quả":
        st.markdown("### Trực quan hóa kết quả")
        centroids = initial_centroids.copy()
        labels_old = None
        while True:
            distances = np.array([[euclid(x, c) for c in centroids] for x in X])
            labels = np.argmin(distances, axis=1)
            if labels_old is not None and np.all(labels == labels_old):
                break
            labels_old = labels.copy()
            new_centroids = []
            for i in range(k):
                pts = X[labels == i]
                new_centroids.append(np.mean(pts, axis=0) if len(pts) > 0 else centroids[i])
            centroids = np.array(new_centroids)

        fig, ax = plt.subplots(figsize=(10, 7))
        colors = ['red', 'green', 'blue', 'orange', 'purple']
        for i in range(k):
            cluster = X[labels == i]
            ax.scatter(cluster[:, 0], cluster[:, 1], s=100, label=f"Cụm C{i+1}", c=colors[i % len(colors)])
            center = centroids[i]
            if len(cluster) > 0:
                radius = max(np.linalg.norm(cluster - center, axis=1)) + 0.15
                circle = mpatches.Circle(center, radius, fill=False, linewidth=2, edgecolor=colors[i % len(colors)], linestyle='--')
                ax.add_patch(circle)
        ax.scatter(centroids[:, 0], centroids[:, 1], marker="X", s=300, c='black', edgecolors="white", linewidth=2, label="Trọng tâm")
        for i, point in enumerate(X):
            ax.text(point[0] + 0.05, point[1] + 0.05, f"x{i+1}", fontsize=11, fontweight='bold')
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.4)
        st.pyplot(fig)

# ===========================================
# GIAO DIỆN CHÍNH
# ===========================================

if 'selected_algorithm' not in st.session_state:
    st.session_state.selected_algorithm = "Tập thô"

with st.sidebar:
    # st.markdown("""
    #     <div style='text-align: center; padding: 1.5rem 0;'>
    #         <div style='font-size: 25px; font-weight: bold;'> CÁC THUẬT TOÁN KHAI PHÁ DỮ LIỆU</div>
    #     </div>
    # """, unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1rem;'>
        <div style='
            font-size: 24px; 
            font-weight: 900; 
            text-transform: uppercase; 
            letter-spacing: 1.5px;
            line-height: 1.4;
            /* Tạo màu chữ Gradient: Trắng -> Tím nhạt */
            background: linear-gradient(90deg, #ffffff 0%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            /* Thêm bóng đổ phát sáng nhẹ */
            filter: drop-shadow(0 0 8px rgba(102, 126, 234, 0.5));
        '>
            CÁC THUẬT TOÁN<br>KHAI PHÁ DỮ LIỆU
        </div>
    </div>
""", unsafe_allow_html=True)
    st.markdown("---")
    
    algorithms = ["Tập thô", "Cây quyết định", "Tập phổ biến", "Phân lớp", "Gom cụm"]
    
    for algo in algorithms:
        if st.button(algo, key=algo, use_container_width=True, type="primary" if st.session_state.selected_algorithm == algo else "secondary"):
            st.session_state.selected_algorithm = algo
            st.rerun()

    st.markdown("---")
    st.sidebar.markdown(
    """
    <div style='text-align: center; color: red; font-size: small;font-weight: bold'>
        Môn học: Khai thác dữ liệu và truyền thông xã hội
    </div>
    """,
    unsafe_allow_html=True
)


selected = st.session_state.selected_algorithm

if selected == "Tập thô":
    render_rough_set()
elif selected == "Cây quyết định":
    render_decision_tree()
elif selected == "Tập phổ biến":
    render_frequent_itemset()
elif selected == "Phân lớp":
    render_naive_bayes()
elif selected == "Gom cụm":
    render_clustering()

