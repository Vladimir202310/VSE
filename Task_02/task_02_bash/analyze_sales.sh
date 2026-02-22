#!/usr/bin/env bash

# использование: ./analyze_sales.sh [sales.txt]

# сколько аргументов?
if [[ $# -gt 1 ]]; then
  echo "много файлов"
  exit
fi

# если аргумент есть — берём его, иначе по умолчанию sales.txt
FILE="${1:-sales.txt}"

# проверяем, что файл существует
if [[ ! -f "$FILE" ]]; then
  echo "файл '$FILE' не найден"
  exit
fi

awk '
{
  # назначаем переменные из столбцов
  date  = $1
  wday  = $2
  item  = $3
  price = $4
  qty   = $5

  sum = price * qty          # выручка по строке

  total += sum               # общая сумма

  day_sum[date]  += sum      # сумма по дате
  day_wday[date] = wday      # день недели для даты

  item_qty[item] += qty      # количество товара
  item_sum[item] += sum      # выручка по товару
}
END {
  # ищем день с максимальной выручкой
  for (d in day_sum) {
    if (day_sum[d] > best_day_sum) {
      best_day_sum = day_sum[d]
      best_date    = d
      best_wday    = day_wday[d]
    }
  }

  # ищем самый популярный товар (по количеству)
  for (it in item_qty) {
    if (item_qty[it] > best_qty) {
      best_qty      = item_qty[it]
      best_item     = it
      best_item_sum = item_sum[it]
    }
  }

  printf "Общая сумма продаж: %.2f\n", total
  printf "День с наибольшей выручкой: %s %s (сумма продаж: %.2f)\n", \
         best_date, best_wday, best_day_sum
  printf "Популярный товар: %s (количество проданных единиц: %d, сумма продаж: %.2f)\n", \
         best_item, best_qty, best_item_sum
}
' "$FILE"
