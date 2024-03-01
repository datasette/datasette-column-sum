import pytest

try:
    from playwright.sync_api import expect
except ImportError:
    expect = None
import pytest
import nest_asyncio

nest_asyncio.apply()

pytestmark = pytest.mark.skipif(expect is None, reason="playwright not installed")


def test_table_cog_menus(ds_server, page):
    page.goto(ds_server + "/data/demo")
    expect(page).to_have_title("data: demo: 4 rows")
    # Should be 4 column cog icons
    assert len(page.query_selector_all("th svg.dropdown-menu-icon")) == 4
    menu = page.query_selector(".dropdown-menu")
    # Menu should start hidden
    assert menu.get_property("style").get_property("display").json_value() == "none"
    # Click on some cogs
    page.query_selector("th.col-category svg").click()
    assert menu.get_property("style").get_property("display").json_value() == "block"
    # Menu should have specific options now
    assert [
        el.text_content() for el in page.query_selector_all(".dropdown-menu li")
    ] == [
        "Sort ascending",
        "Sort descending",
        "Facet by this",
        "Hide this column",
        "Show all columns",
        "Show not-blank rows",
        "sum(value_int) by category",
        "sum(value_float) by category",
    ]
    # Now try clicking on value_int and value_float
    for column in ("value_int", "value_float"):
        page.query_selector(f"th.col-{column} svg").click()
        assert (
            menu.get_property("style").get_property("display").json_value() == "block"
        )
        assert [
            el.text_content() for el in page.query_selector_all(".dropdown-menu li")
        ] == [
            "Sort ascending",
            "Sort descending",
            "Facet by this",
            "Hide this column",
            "Show all columns",
            "Show not-blank rows",
            f"sum({column})",
        ]
