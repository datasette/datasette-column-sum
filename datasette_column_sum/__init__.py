from datasette import hookimpl

JS = """
document.addEventListener('datasette_init', function(ev) {
  ev.detail.registerPlugin('column-name-plugin', {
    version: 0.1,
    makeColumnActions: (columnDetails) => {
      console.log({columnDetails});
      const numericColumns = Array.from(
        document.querySelectorAll('[data-column-type="float"],[data-column-type="integer"]')
      ).filter(el => el.dataset.isPk != "1").map((el) => el.dataset.column);
      console.log({numericColumns});
      if (columnDetails.columnType == 'float' || columnDetails.columnType == 'integer') {
        const sql = `select sum(${columnDetails.columnName}) from {table}`;
        return [
          {
            label: `sum(${columnDetails.columnName})`,
            onClick: () => {
              location.href = '/{database}?sql=' + encodeURIComponent(sql);
            }
          }
        ];
      }
      if (columnDetails.columnType == 'text' && numericColumns.length) {
        // Add options for every other numeric column
        return numericColumns.map((name) => ({
          label: 'sum(' + name + ') by ' + columnDetails.columnName,
          onClick: () => {
            const sql = `select ${columnDetails.columnName}, sum(${name}) from {table} group by ${columnDetails.columnName}`;
            location.href = '/{database}?sql=' + encodeURIComponent(sql);
          }
        }));
      }
      return [];
    }
  });
});
"""


@hookimpl
def extra_body_script(database, table):
    if database and table:
        return {"script": JS.replace("{database}", database).replace("{table}", table)}
