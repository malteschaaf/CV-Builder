-- columns.lua

local function latex_escape(s)
    return s
      :gsub("\\", "\\textbackslash{}")
      :gsub("%%", "\\%%")
      :gsub("&", "\\&")
      :gsub("#", "\\#")
      :gsub("_", "\\_")
      :gsub("{", "\\{")
      :gsub("}", "\\}")
  end
  
  local function make_columns(columns)
    local ncols = #columns
    local latex =
      "\\begin{tabularx}{\\linewidth}{@{}" ..
      string.rep("X", ncols) ..
      "@{}}\n"
  
    local max_rows = 0
    for _, col in ipairs(columns) do
      max_rows = math.max(max_rows, #col)
    end
  
    for r = 1, max_rows do
      for c = 1, ncols do
        local v = columns[c][r] or ""
        latex = latex .. latex_escape(v)
        latex = latex .. (c < ncols and " & " or " \\\\\n")
      end
    end
  
    latex = latex .. "\\end{tabularx}\n"
    return pandoc.RawBlock("latex", latex)
  end
  
  function Pandoc(doc)
    local out = {}
    local i = 1
  
    while i <= #doc.blocks do
      local blk = doc.blocks[i]
  
      -- Detect: BulletList followed by HR → column block
      if blk.t == "BulletList"
         and doc.blocks[i + 1]
         and doc.blocks[i + 1].t == "HorizontalRule" then
  
        local columns = {}
  
        while true do
          -- Collect one column
          local col = {}
          for _, item in ipairs(doc.blocks[i].content) do
            table.insert(col, pandoc.utils.stringify(item))
          end
          table.insert(columns, col)
  
          i = i + 1 -- move past BulletList
  
          -- Check if another HR + BulletList follows
          if not (
            doc.blocks[i]
            and doc.blocks[i].t == "HorizontalRule"
            and doc.blocks[i + 1]
            and doc.blocks[i + 1].t == "BulletList"
          ) then
            break
          end
  
          i = i + 1 -- skip HR
        end
  
        -- Insert columns block
        table.insert(out, make_columns(columns))
  
        -- ⚠️ WICHTIG: kein weiteres i = i + 1 hier
  
      else
        table.insert(out, blk)
        i = i + 1
      end
    end
  
    return pandoc.Pandoc(out, doc.meta)
  end
  