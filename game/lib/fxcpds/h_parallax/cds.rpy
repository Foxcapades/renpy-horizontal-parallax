python early:

    def _exec_h_parallax_cds(values):
        name, layers, opts = values

        renpy.image(name, HParallax(*layers, **opts))

    def _parse_h_parallax_cds(lexer, **opts):
        name = lexer.name()

        if name is None:
            lexer.error("h_parallax name is required")

        lexer.expect_block(f'h_parallax {name}')

        sub_l  = lexer.subblock_lexer()
        layers = []
        opts   = {}

        while sub_l.advance():
            check = sub_l.checkpoint()
            stmt = sub_l.match(r'^([\w]+|"[\w/\.\-]+")')

            if stmt is None:
                sub_l.error("invalid or unrecognized statement")

            # Parse the optional 'direction' property.
            elif stmt == 'direction':
                direction = sub_l.require(sub_l.string)

                if direction is None:
                    if sub_l.eol():
                        sub_l.error('missing direction value')
                    else:
                        sub_l.error('invalid direction value')

                if not (direction == 'left' or direction == 'right'):
                    sub_l.error("direction must be either 'left' or 'right'")
                else:
                    opts['direction'] = direction

                sub_l.expect_eol()

            # Parse the optional 'render_delay' property.
            elif stmt == 'render_delay':
                render_delay = sub_l.require(sub_l.float)

                if render_delay is None:
                    sub_l.error('missing render_delay value')

                render_delay = float(render_delay)

                if render_delay < 0.0:
                    sub_l.error("render_delay must be greater than or equal to 0.0")
                else:
                    opts["render_delay"] = render_delay

                sub_l.expect_eol()

            # Parse the optional 'height' property.
            elif stmt == 'height':
                check = sub_l.checkpoint()
                height = sub_l.require(sub_l.integer)

                if height is None:
                    sub_l.error("missing height value")

                height = int(height)

                if height < 1:
                    sub_l.revert(check)
                    sub_l.error("height must be greater than or equal to 1")
                else:
                    opts["height"] = height

                sub_l.expect_eol()

            # Parse the optional 'width' property.
            elif stmt == 'width':
                check = sub_l.checkpoint()
                width = sub_l.require(sub_l.integer)

                if width is None:
                    sub_l.error("missing width value")

                width = int(width)

                if width < 1:
                    sub_l.revert(check)
                    sub_l.error("width must be greater than or equal to 1")
                else:
                    opts["width"] = width

                sub_l.expect_eol()

            # Parse an image line
            elif stmt.startswith('"'):
                image = stmt.strip('"')

                if len(image) == 0:
                    sub_l.error('image path/name cannot be empty')

                speed = sub_l.float()

                if speed is None:
                    sub_l.error('missing scroll speed value')

                speed = float(speed)

                if speed < 0.0:
                    sub_l.error('speed must be greater than or equal to zero')
                else:
                    layers.append((image, speed))

                sub_l.expect_eol()

            else:
                sub_l.revert(check)
                sub_l.error(f'unrecognized statement: "{stmt}"')

        if len(layers) == 0:
            lexer.error("h_parallax requires at least one layer")

        return (name, layers, opts)

    renpy.register_statement(
        name = "h_parallax",
        block = True,
        parse = _parse_h_parallax_cds,
        execute_init = _exec_h_parallax_cds,
    )