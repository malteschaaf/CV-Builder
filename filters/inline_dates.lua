-- Function to escape LaTeX special characters
local function escape_latex(str)
  local replacements = {
      ["\\"] = "\\textbackslash{}",
      ["{"] = "\\{",
      ["}"] = "\\}",
      ["&"] = "\\&",
      ["%"] = "\\%",
      ["$"] = "\\$",
      ["#"] = "\\#",
      ["_"] = "\\_",
      ["~"] = "\\textasciitilde{}",
      ["^"] = "\\textasciicircum{}"
  }
  return (str:gsub(".", replacements))
end

-- Main Pandoc filter function
-- This function processes the document to find level 2 and 3 headers followed by blockquotes
-- and converts them into LaTeX \HeadingWithMetadata commands, escaping special characters as needed.
function Pandoc(doc)
  local blocks = {}
  local i = 1
  while i <= #doc.blocks do
      local b = doc.blocks[i]

      -- Check for level 2 or 3 headers
      if b.t == "Header" and (b.level == 2 or b.level == 3) then
          local header = pandoc.utils.stringify(b.content)
          local right_aligned_text = ""

          -- Check if the next block is a BlockQuote
          if i + 1 <= #doc.blocks and doc.blocks[i + 1].t == "BlockQuote" then
              local quote = doc.blocks[i + 1].content
              right_aligned_text = pandoc.utils.stringify(quote)
              i = i + 1
          end

          -- Escape LaTeX special characters
          header = escape_latex(header)
          right_aligned_text = escape_latex(right_aligned_text)

          -- Insert the LaTeX command
          table.insert(blocks, pandoc.RawBlock("latex",
              string.format("\\HeadingWithNote{%i}{%s}{%s}", b.level, header, right_aligned_text)))

      else
          table.insert(blocks, b)
      end

      i = i + 1
  end

  return pandoc.Pandoc(blocks, doc.meta)
end