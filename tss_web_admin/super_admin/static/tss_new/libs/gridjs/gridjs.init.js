new gridjs.Grid({
    columns: ["Employee", "Time off type", "Description", "Start date", "End date", "Duration", "Status"],
    pagination: {
        limit: 5
    },
    sort: !0,
    search: !0,
    data: [
        ["Amritha", "Paid time off", "Headache", "Dec 30, 2022", "Dec 31, 2022", "1 Day", "Pending"],
        ["Amar", "Unpaid", "Fever", "Feb 7,2024", "Feb 8,2024", "1 Day", "Pending"],
        ["Jiyad", "Paid time off", "Headache", "Dec 30, 2022", "Dec 31, 2022", "1 Day", "Pending"],
        ["Amritha", "Unpaid", "Fever", "Feb 7,2024", "Feb 8,2024", "1 Day", "Pending"],
        ["Anirudh", "Paid time off", "Headache", "Dec 30, 2022", "Dec 31, 2022", "1 Day", "Pending"],
        ["Amritha", "Unpaid", "Fever", "Feb 7,2024", "Feb 8,2024", "1 Day", "Pending"],
        ["Jiyad", "Paid time off", "Headache", "Dec 30, 2022", "Dec 31, 2022", "1 Day", "Second Approve"],
        ["Amritha", "Unpaid", "Fever", "Feb 7,2024", "Feb 8,2024", "1 Day", "Pending"],
        ["Amar", "Paid time off", "Headache", "Dec 30, 2022", "Dec 31, 2022", "1 Day", "Second Approve"],
        ["Jiyad", "Unpaid", "Fever", "Feb 7,2024", "Feb 8,2024", "1 Day", "Pending"],
    ]
}).render(document.getElementById("table-search"))

